import pytz
from copy import deepcopy

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django import forms
from django.conf import settings
from django.forms import ValidationError
from django.forms.utils import ErrorList
from django.utils import timezone

from edc_constants.constants import YES, NO
from edc_base.utils import formatted_age
from edc_map.site_mappers import site_mappers
from edc_constants.constants import NOT_APPLICABLE


from member.constants import HEAD_OF_HOUSEHOLD
from member.models import HouseholdInfo
from household.models import HouseholdLogEntry
from survey.models import Survey
from member.models import HouseholdHeadEligibility

from ..constants import BASELINE_SURVEY
from ..models import SubjectConsent

tz = pytz.timezone(settings.TIME_ZONE)


class ConsentFormMixin:

    def clean(self):
        cleaned_data = super(ConsentFormMixin, self).clean()
        self.clean_consent_with_household_member()
        self.clean_citizen_with_legally_married()
        self.limit_edit_to_current_community()
        self.validate_household_log_entry()
        self.limit_edit_to_current_survey()
        self.household_info()
        try:
            model = self._meta.model.proxy_for_model
        except AttributeError:
            model = self._meta.model
        household_member = cleaned_data.get('household_member')
        if household_member:
            subject_consent = model(**cleaned_data)
            subject_consent.matches_enrollment_checklist(
                subject_consent, exception_cls=forms.ValidationError)
            try:
                HouseholdHeadEligibility.objects.get(household_structure=household_member.household_structure)
            except HouseholdHeadEligibility.DoesNotExist:
                raise forms.ValidationError(
                    'Please fill household head eligibility form before completing subject consent.',
                    code='invalid')
        return cleaned_data

    def clean_consent_matches_enrollment(self):
        household_member = self.cleaned_data.get("household_member")
        if not SubjectConsent.objects.filter(
                household_member__internal_identifier=household_member.internal_identifier).exclude(
                household_member=household_member).exists():
            consent_datetime = self.cleaned_data.get("consent_datetime", self.instance.consent_datetime)
            options = deepcopy(self.cleaned_data)
            options.update({'consent_datetime': consent_datetime})
            self.instance.matches_enrollment_checklist(
                SubjectConsent(**options), forms.ValidationError)
            self.instance.matches_hic_enrollment(
                SubjectConsent(**options), household_member, forms.ValidationError)

    def clean_consent_with_household_member(self):
        """Validates subject consent values against household member values."""
        initials = self.cleaned_data.get("initials")
        first_name = self.cleaned_data.get("first_name")
        gender = self.cleaned_data.get("gender")
        household_member = self.cleaned_data.get("household_member")
        if household_member:
            if initials != household_member.initials:
                raise forms.ValidationError(
                    'Initials do not match with household member. %(initials)s <> %(hm_initials)s',
                    params={'hm_initials': household_member.initials, 'initials': initials},
                    code='invalid')
            if household_member.first_name != first_name:
                raise forms.ValidationError(
                    'First name does not match with household member. Got %(first_name)s <> %(hm_first_name)s',
                    params={'hm_first_name': household_member.first_name, 'first_name': first_name},
                    code='invalid')
            if household_member.gender != gender:
                raise forms.ValidationError(
                    'Gender does not match with household member. Got %(gender)s <> %(hm_gender)s',
                    params={'hm_gender': household_member.gender, 'gender': gender},
                    code='invalid')

    def clean_citizen_with_legally_married(self):
        citizen = self.cleaned_data.get('citizen')
        legal_marriage = self.cleaned_data.get('legal_marriage')
        marriage_certificate = self.cleaned_data.get('marriage_certificate')
        marriage_certificate_no = self.cleaned_data.get('marriage_certificate_no')
        if citizen == NO:
            if legal_marriage == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You wrote subject is NOT a citizen. Is the subject legally married to a citizen?',
                    code='invalid')
            elif legal_marriage == NO:
                raise forms.ValidationError(
                    'You wrote subject is NOT a citizen and is NOT legally married to a citizen. '
                    'Subject cannot be consented',
                    code='invalid')
            elif legal_marriage == YES and marriage_certificate != YES:
                raise forms.ValidationError(
                    'You wrote subject is NOT a citizen. Subject needs to produce a marriage certificate',
                    code='invalid')
            elif legal_marriage == YES and marriage_certificate == YES:
                if not marriage_certificate_no:
                    raise forms.ValidationError(
                        'You wrote subject is NOT a citizen and has marriage certificate. Please provide certificate number.',
                        code='invalid')

        if citizen == YES:
            if legal_marriage != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You wrote subject is a citizen. That subject is legally married to a citizen is not applicable.',
                    code='invalid')
            elif marriage_certificate != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You wrote subject is a citizen. The subject\'s marriage certificate is not applicable.',
                    code='invalid')

    def limit_edit_to_current_survey(self):
        household_member = self.cleaned_data.get("household_member")
        if household_member:
            try:
                limit = settings.LIMIT_EDIT_TO_CURRENT_SURVEY
            except AttributeError:
                limit = False
            if limit:
                current_survey = Survey.objects.current_survey()
                if household_member.household_structure.survey != current_survey:
                    raise forms.ValidationError(
                        'Form may not be saved. Only data from %(current_survey)s '
                        'may be added/changed. (LIMIT_EDIT_TO_CURRENT_SURVEY)',
                        params={'current_survey': current_survey},
                        code='invalid')

    def limit_edit_to_current_community(self):
        household_member = self.cleaned_data.get("household_member")
        if household_member:
            try:
                limit = settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY
            except AttributeError:
                limit = False
            if limit:
                mapper_community = site_mappers.get_mapper(site_mappers.current_map_area).map_area
                community = household_member.household_structure.household.plot.community
                if community != mapper_community:
                    raise forms.ValidationError(
                        'Form may not be saved. Only data from \'%(mapper_community)s\' may be added/changed on '
                        'this device. Got %(community)s. (LIMIT_EDIT_TO_CURRENT_COMMUNITY)',
                        params={'mapper_community': mapper_community, 'community': community}, code='invalid')

    def household_info(self):
        household_member = self.cleaned_data.get('household_member')
        if household_member:
            if (household_member.relation == HEAD_OF_HOUSEHOLD and
                    household_member.household_structure.survey.survey_slug == BASELINE_SURVEY):
                try:
                    HouseholdInfo.objects.get(household_member=household_member)
                except HouseholdInfo.DoesNotExist:
                    raise forms.ValidationError(
                        'Complete \'%(model)s\' before consenting head of household',
                        params={'model': HouseholdInfo._meta.verbose_name}, code='invalid')

    def clean_household_member(self):
        household_member = self.cleaned_data.get("household_member")
        if not household_member:
            raise forms.ValidationError("Please select the household member.")
        return household_member

    @property
    def personal_details_changed(self):
        household_member = self.cleaned_data.get("household_member")
        if household_member.personal_details_changed == YES:
            return True
        return False

    def validate_legal_marriage(self):
        if self.cleaned_data.get("legal_marriage") == NO:
            if not (self.cleaned_data.get("marriage_certificate") in [YES, NO]):
                raise forms.ValidationError("if married not to a citizen, marriage_certificate proof should be YES or NO.")

    def clean_identity_with_unique_fields(self):
        identity = self.cleaned_data.get('identity')
        first_name = self.cleaned_data.get('first_name')
        initials = self.cleaned_data.get('initials')
        dob = self.cleaned_data.get('dob')
        unique_together_form = self.unique_together_string(first_name, initials, dob)
        for consent in self._meta.model.objects.filter(identity=identity):
            unique_together_model = self.unique_together_string(consent.first_name, consent.initials, consent.dob)
            if not self.personal_details_changed:
                if unique_together_form != unique_together_model:
                    raise ValidationError(
                        'Identity \'%(identity)s\' is already in use by subject %(subject_identifier)s. '
                        'Please resolve.',
                        params={'subject_identifier': consent.subject_identifier, 'identity': identity},
                        code='invalid')
        for consent in self._meta.model.objects.filter(first_name=first_name, initials=initials, dob=dob):
            if consent.identity != identity:
                raise ValidationError(
                    'Subject\'s identity was previously reported as \'%(existing_identity)s\'. '
                    'You wrote \'%(identity)s\'. Please resolve.',
                    params={'existing_identity': consent.identity, 'identity': identity},
                    code='invalid')

    def clean_dob_relative_to_consent_datetime(self):
        """Validates that the dob is within the bounds of MIN and MAX set on the model."""
        dob = self.cleaned_data.get('dob')
        consent_datetime = self.cleaned_data.get('consent_datetime', self.instance.consent_datetime)
        if not consent_datetime:
            self._errors["consent_datetime"] = ErrorList([u"This field is required. Please fill consent date and time."])
            raise ValidationError('Please correct the errors below.')

        consent_date = timezone.localtime(consent_datetime).date()
        MIN_AGE_OF_CONSENT = self.get_model_attr('MIN_AGE_OF_CONSENT')
        MAX_AGE_OF_CONSENT = self.get_model_attr('MAX_AGE_OF_CONSENT')
        identity = self.cleaned_data.get('identity')
        consents = SubjectConsent.objects.filter(
            household_member__registered_subject__identity=identity).order_by('-created')
        if not consents:
            rdelta = relativedelta(consent_date, dob)
            if rdelta.years < MIN_AGE_OF_CONSENT:
                raise ValidationError(
                    'Subject\'s age is %(age)s. Subject is not eligible for consent.',
                    params={'age': formatted_age(dob, consent_date)},
                    code='invalid')
            if rdelta.years > MAX_AGE_OF_CONSENT:
                raise ValidationError(
                    'Subject\'s age is %(age)s. Subject is not eligible for consent.',
                    params={'age': formatted_age(dob, consent_date)},
                    code='invalid')

    def validate_household_log_entry(self):
        household_member = self.cleaned_data.get("household_member")
        household_structure = household_member.household_structure
        try:
            SubjectConsent.objects.get(household_member=household_member)
        except SubjectConsent.DoesNotExist:
            try:
                log_entry = HouseholdLogEntry.objects.filter(
                    household_log__household_structure=household_structure).order_by('created').last()
                if not log_entry.report_datetime == datetime.today().date():
                    raise ValidationError(
                        'Please fill household log entry before completing subject consent.',
                        params={},
                        code='invalid')
            except HouseholdLogEntry.DoesNotExist:
                raise ValidationError(
                    'Please fill household log entry before completing subject consent.',
                    params={},
                    code='invalid')
            except AttributeError:
                raise ValidationError(
                    'Please fill household log entry before completing subject consent.',
                    params={},
                    code='invalid')


class SubjectConsentForm(ConsentFormMixin, forms.ModelForm):

    class Meta:
        model = SubjectConsent
        fields = '__all__'
