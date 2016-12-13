from datetime import date
from dateutil.relativedelta import relativedelta

from django.apps import apps as django_apps
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_consent.field_mixins.bw import IdentityFieldsMixin
from edc_consent.field_mixins import (
    ReviewFieldsMixin, PersonalFieldsMixin, VulnerabilityFieldsMixin,
    SampleCollectionFieldsMixin, CitizenFieldsMixin)
from edc_consent.managers import ObjectConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.constants import YES, NO
from edc_offstudy.model_mixins import OffstudyMixin

from member.constants import BHS_ELIGIBLE, BHS
from member.exceptions import MemberStatusError
from member.models import EnrollmentChecklist

from .model_mixins import SubjectConsentMixin as BcppSubjectConsentMixin


class BaseSubjectConsent(models.Model):

    def matches_hic_enrollment(self, subject_consent, household_member, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        HicEnrollment = django_apps.get_model('bcpp_subject', 'HicEnrollment')
        if HicEnrollment.objects.filter(subject_visit__household_member=household_member).exists():
            hic_enrollment = HicEnrollment.objects.get(subject_visit__household_member=household_member)
            # consent_datetime does not exist in cleaned_data as it not editable.
            # if subject_consent.dob != hic_enrollment.dob or
            # subject_consent.consent_datetime != hic_enrollment.consent_datetime:
            if subject_consent.dob != hic_enrollment.dob:
                raise exception_cls('An HicEnrollment form already exists for this '
                                    'Subject. So \'dob\' cannot be changed.')

    def matches_enrollment_checklist(self, subject_consent, exception_cls=None):
        """Matches values in this consent against the enrollment checklist.

        ..note:: the enrollment checklist is required for consent, so always exists."""
        # enrollment checklist is only filled for the same survey as the consent
        household_member = self.household_member
        exception_cls = exception_cls or ValidationError
        try:
            enrollment_checklist = EnrollmentChecklist.objects.get(
                household_member__registered_subject=subject_consent.household_member.registered_subject,
                is_eligible=True)
            household_member = enrollment_checklist.household_member
        except EnrollmentChecklist.DoesNotExist:
            raise exception_cls(
                'A valid Enrollment Checklist not found (is_eligible). The Enrollment Checklist is required before'
                ' consent.')
        self.validate_guardian_dob(enrollment_checklist, subject_consent, exception_cls)
        self.validate_citizen_literacy_nd_legal_marriage(enrollment_checklist, subject_consent, exception_cls)
        if not household_member.eligible_subject:
            raise exception_cls('Subject is not eligible or has not been confirmed eligible '
                                'for BHS. Perhaps catch this in the forms.py. Got {0}'.format(household_member))
        return True

    def validate_guardian_dob(self, enrollment_checklist, subject_consent, exception_cls):
        if enrollment_checklist.dob != subject_consent.dob:
            raise exception_cls('Dob does not match that on the enrollment checklist')
        if not self.household_member.personal_details_changed == YES:
            if enrollment_checklist.initials != subject_consent.initials:
                raise exception_cls('Initials do not match those on the enrollment checklist')
        if subject_consent.consent_datetime:
            if subject_consent.minor:
                if (enrollment_checklist.guardian == YES and
                        not (subject_consent.minor and subject_consent.guardian_name)):
                    raise exception_cls('Enrollment Checklist indicates that subject is a minor with guardian '
                                        'available, but the consent does not indicate this.')
        if enrollment_checklist.gender != subject_consent.gender:
            raise exception_cls('Gender does not match that in the enrollment checklist')

    def validate_citizen_literacy_nd_legal_marriage(self, enrollment_checklist, subject_consent, exception_cls):
        if enrollment_checklist.citizen != subject_consent.citizen:
            raise exception_cls(
                'You wrote subject is a %(citizen)s citizen. This does not match the enrollment checklist.',
                params={"citizen": '' if subject_consent.citizen == YES else 'NOT'})
        if (enrollment_checklist.literacy == YES and
                not (subject_consent.is_literate == YES or (subject_consent.is_literate == NO) and
                     subject_consent.witness_name)):
            raise exception_cls('Answer to whether this subject is literate/not literate but with a '
                                'literate witness, does not match that in enrollment checklist.')
        if ((enrollment_checklist.legal_marriage == YES and
                enrollment_checklist.marriage_certificate == YES) and not (
                subject_consent.legal_marriage == YES and
                subject_consent.marriage_certificate == YES)):
            raise exception_cls('Enrollment Checklist indicates that this subject is married '
                                'to a citizen with a valid marriage certificate, but the '
                                'consent does not indicate this.')

    @property
    def survey_of_consent(self):
        return self.survey.survey_name

    @property
    def minor(self):
        age_at_consent = relativedelta(
            date(self.consent_datetime.year,
                 self.consent_datetime.month,
                 self.consent_datetime.day),
            self.dob).years
        return age_at_consent >= 16 and age_at_consent <= 17

    @classmethod
    def get_consent_update_model(self):
        raise TypeError(
            'The ConsentUpdateModel is required. Specify a class method get_consent_update_model() on the model to '
            'return the ConsentUpdateModel class.')

    def bypass_for_edit_dispatched_as_item(self, using=None, update_fields=None):
        """Allow bypass only if doing consent verification."""
        # requery myself
        obj = self.__class__.objects.using(using).get(pk=self.pk)
        # dont allow values in these fields to change if dispatched
        may_not_change_these_fields = [(k, v) for k, v in obj.__dict__.iteritems() if k not in [
            'is_verified_datetime', 'is_verified']]
        for k, v in may_not_change_these_fields:
            if k[0] != '_':
                if getattr(self, k) != v:
                    return False
        return True

    def save(self, *args, **kwargs):
        if not self.id:
            self.registered_subject = self.household_member.registered_subject
            self.survey = self.household_member.household_structure.survey
        consents = self.__class__.objects.filter(
            household_member__internal_identifier=self.household_member.internal_identifier).exclude(
            household_member=self.household_member)
        if not consents.exists():
            if not self.id:
                expected_member_status = BHS_ELIGIBLE
            else:
                expected_member_status = BHS
            subject_identifier = self.household_member.get_subject_identifier()
            try:
                self.__class__.objects.filter(subject_identifier=subject_identifier).latest('consent_datetime')
                expected_member_status = BHS
                self.subject_identifier = subject_identifier
            except ObjectDoesNotExist:
                pass
            if self.household_member.member_status != expected_member_status:
                raise MemberStatusError('Expected member status to be {0}. Got {1} for {2}.'.format(
                    expected_member_status, self.household_member.member_status, self.household_member))
            self.is_minor = YES if self.minor else NO
            self.matches_enrollment_checklist(self)
            self.matches_hic_enrollment(self, self.household_member)
        else:
            self.registered_subject = consents[0].registered_subject
            self.subject_identifier = consents[0].subject_identifier
        self.community = self.household_member.household_structure.household.plot.community
        super(BaseSubjectConsent, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class SubjectConsent(
        ConsentModelMixin, OffstudyMixin,
        BcppSubjectConsentMixin, IdentityFieldsMixin, ReviewFieldsMixin, PersonalFieldsMixin,
        SampleCollectionFieldsMixin, CitizenFieldsMixin, VulnerabilityFieldsMixin,
        BaseUuidModel):

    """ A model completed by the user that captures the ICF."""

    objects = ObjectConsentManager()

    history = HistoricalRecords()

    class Meta:
        app_label = 'bcpp_subject'
        get_latest_by = 'consent_datetime'
        unique_together = (('subject_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
        ordering = ('-created', )
