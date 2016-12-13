from dateutil.relativedelta import relativedelta

from django.apps import apps as django_apps
from django.db import models
from django.core.exceptions import ValidationError

from edc_base.model.models import HistoricalRecords
from edc_base.model.validators import datetime_not_future
from edc_consent.validators import AgeTodayValidator
from edc_constants.choices import YES_NO
from edc_constants.constants import YES, NO, NEG

from .model_mixins import CrfModelMixin
from .subject_consent import SubjectConsent


class HicEnrollment (CrfModelMixin):

    hic_permission = models.CharField(
        verbose_name='Is it okay for the project to visit you every year for '
                     'the next three years for further questions and testing?',
        max_length=25,
        choices=YES_NO,
        help_text='If \'No\', subject is not eligible.'
    )

    permanent_resident = models.NullBooleanField(
        default=None,
        null=True,
        blank=True,
        help_text='From Residency and Mobility. Eligible if Yes.'
    )

    intend_residency = models.NullBooleanField(
        default=None,
        null=True,
        blank=True,
        help_text='From Residency and Mobility. Eligible if No.'
    )

    hiv_status_today = models.CharField(
        max_length=50,
        help_text="From Today's HIV Result. Eligible if Negative.",
    )

    dob = models.DateField(
        verbose_name="Date of birth",
        validators=[AgeTodayValidator(16, 64)],
        default=None,
        help_text="Format is YYYY-MM-DD. From Subject Consent.",
    )

    household_residency = models.NullBooleanField(
        default=None,
        null=True,
        blank=True,
        help_text='Is Participant a Household Member. Eligible if Yes.'
    )

    citizen_or_spouse = models.NullBooleanField(
        default=None,
        help_text='From Subject Consent. Is participant a citizen, or married to citizen '
                  'with a valid marriage certificate?',
    )

    locator_information = models.NullBooleanField(
        default=None,
        null=True,
        blank=True,
        help_text='From Subject Locator. Is the locator form filled and all '
                  'necessary contact information collected?',
    )

    consent_datetime = models.DateTimeField(
        verbose_name="Consent date and time",
        validators=[
            datetime_not_future, ],
        help_text="From Subject Consent."
    )

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.hic_permission.lower() == 'yes':
            # Only enforce the criteria if subjectt agrees to enroll in HIC
            self.permanent_resident = self.is_permanent_resident()
            self.intend_residency = self.is_intended_residency()
            self.household_residency = self.is_household_residency()
            self.locator_information = self.is_locator_information()
            self.citizen_or_spouse = self.is_citizen_or_spouse()
            self.hiv_status_today = self.get_hiv_status_today()
        update_fields = kwargs.get('update_fields')
        if not update_fields:
            dob, consent_datetime = self.get_dob_consent_datetime()
            self.dob = dob
            self.consent_datetime = consent_datetime
        super(HicEnrollment, self).save(*args, **kwargs)

    def is_permanent_resident(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        ResidencyMobility = django_apps.get_model('bcpp_subject', 'ResidencyMobility')
        residency_mobility = ResidencyMobility.objects.filter(subject_visit=self.subject_visit)
        if residency_mobility.exists():
            if residency_mobility[0].permanent_resident == YES:
                return True
            else:
                raise exception_cls('Please review \'residency_mobility\' in ResidencyMobility '
                                    'form before proceeding with this one.')
        else:
            raise exception_cls('Please fill ResidencyMobility form before proceeding with this one.')

    def is_intended_residency(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        ResidencyMobility = django_apps.get_model('bcpp_subject', 'ResidencyMobility')
        residency_mobility = ResidencyMobility.objects.filter(subject_visit=self.subject_visit)
        if residency_mobility.exists():
            if residency_mobility[0].intend_residency == NO:
                return True
            else:
                raise exception_cls('Please review \'intend_residency\' in ResidencyMobility '
                                    'form before proceeding with this one.')
        else:
            raise exception_cls('Please fill ResidencyMobility form before proceeding with this one.')

    def get_hiv_status_today(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        HivResult = django_apps.get_model('bcpp_subject', 'HivResult')
        ElisaHivResult = django_apps.get_model('bcpp_subject', 'ElisaHivResult')
        hiv_result = HivResult.objects.filter(subject_visit=self.subject_visit)
        elisa_result = ElisaHivResult.objects.filter(subject_visit=self.subject_visit)
        if hiv_result.exists():
            if (hiv_result[0].hiv_result == NEG or (
                    elisa_result.exists() and elisa_result[0].hiv_result == NEG)):
                return NEG
            else:
                raise exception_cls(
                    'Please review \'hiv_result\' in Today\'s Hiv Result form '
                    'or in Elisa Hiv Result before proceeding with this one.')
        else:
            raise exception_cls('Please fill Today\'s Hiv Result form before proceeding with this one.')

    def get_dob_consent_datetime(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        subject_consent = SubjectConsent.objects.filter(
            subject_identifier=self.subject_visit.appointment.registered_subject.subject_identifier)
        if subject_consent.exists():
            if subject_consent[0].dob and subject_consent[0].consent_datetime:
                return (subject_consent[0].dob, subject_consent[0].consent_datetime)
            else:
                raise exception_cls('Please review \'dob\' and \'consent_datetime\' in SubjectConsent '
                                    'form before proceeding with this one.')
        else:
            raise exception_cls('Please fill SubjectConsent form before proceeding with this one.')

    def is_household_residency(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        if self.subject_visit.household_member:
            return True
        else:
            raise exception_cls('This form has to be attached by to a household member. Currently it is not.')

    def is_citizen_or_spouse(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        try:
            subject_consent = SubjectConsent.objects.get(household_member=self.subject_visit.household_member)
            if ((subject_consent.citizen == YES) or (
                    subject_consent.legal_marriage == YES and
                    subject_consent.marriage_certificate == YES)):
                return True
            else:
                raise exception_cls('Please review \'citizen\', \'legal_marriage\' and '
                                    '\'marriage_certificate\' in SubjectConsent for {}. Got {}, {}, {}'.format(
                                        subject_consent,
                                        subject_consent.citizen,
                                        subject_consent.legal_marriage,
                                        subject_consent.marriage_certificate
                                    ))
        except SubjectConsent.DoesNotExist:
            raise exception_cls('Please fill SubjectConsent form before proceeding with this one.')

    def is_locator_information(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        SubjectLocator = django_apps.get_model('bcpp_subject', 'SubjectLocator')
        subject_locator = SubjectLocator.objects.filter(
            registered_subject=self.subject_visit.appointment.registered_subject)
        # At least some information to contact the person should be available
        if subject_locator.exists():
            if (subject_locator[0].subject_cell or
                    subject_locator[0].subject_cell_alt or
                    subject_locator[0].subject_phone or
                    subject_locator[0].mail_address or
                    subject_locator[0].physical_address or
                    subject_locator[0].subject_cell or
                    subject_locator[0].subject_cell_alt or
                    subject_locator[0].subject_phone or
                    subject_locator[0].subject_phone_alt or
                    subject_locator[0].subject_work_place or
                    subject_locator[0].subject_work_phone or
                    subject_locator[0].contact_physical_address or
                    subject_locator[0].contact_cell or
                    subject_locator[0].contact_phone):
                return True
            else:
                raise exception_cls('Please review SubjectLocator to ensure there is some '
                                    'way to contact the participant form before proceeding with this one.')
        else:
            raise exception_cls('Please fill SubjectLocator form before proceeding with this one.')

    def may_contact(self):
        if self.hic_permission == YES:
            return '<img src="/static/admin/img/icon-yes.gif" alt="True" />'
        else:
            return '<img src="/static/admin/img/icon-no.gif" alt="False" />'
    may_contact.allow_tags = True

    def age(self):
        return relativedelta(self.consent_datetime.date(), self.dob).years
    age.allow_tags = True

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Hic Enrollment"
        verbose_name_plural = "Hic Enrollment"
