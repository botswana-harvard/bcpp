from django import forms

from edc_constants.constants import MALE, FEMALE

from ..models import Demographics, SubjectConsent

from .form_mixins import SubjectModelFormMixin


class DemographicsForm(SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(DemographicsForm, self).clean()
        # validating ethnic group
        if cleaned_data.get('ethnic') and cleaned_data.get('religion'):
            ethnic_count = cleaned_data.get('ethnic').count()
            religion_count = cleaned_data.get('religion').count()
            if ethnic_count > 1 or religion_count > 1:
                raise forms.ValidationError('Can only belong to one religion or ethnic group')
        # validating living with
        if cleaned_data.get('live_with'):
            if cleaned_data.get('live_with').count() > 1:
                for item in cleaned_data.get('live_with'):
                    if str(item) == "Alone" or str(item) == 'Don\'t want to answer':
                        raise forms.ValidationError(
                            "\"Don't want to answer\" or \"Alone\" options can only be selected singularly")
        # validating unmarried
        if cleaned_data.get('marital_status', None) != 'Married' and cleaned_data.get('num_wives', None):
            raise forms.ValidationError('If participant is not married, do not give number of wives')
        if cleaned_data.get('marital_status', None) != 'Married' and cleaned_data.get('husband_wives', None):
            raise forms.ValidationError('If participant is not married, the number of wives is not required')
        self.marital_status_married()

        return cleaned_data

    def marital_status_married(self):
        cleaned_data = self.cleaned_data
        # validating if married
        if cleaned_data.get('marital_status') == 'Married':
            husband_wives = cleaned_data.get('husband_wives', 0)
            num_wives = cleaned_data.get('num_wives', 0)
            subject_visit = cleaned_data.get('subject_visit')
            subject_identifier = subject_visit.subject_identifier
            consent = SubjectConsent.objects.filter(
                household_member__registered_subject__subject_identifier=subject_identifier).last()
            if num_wives > 0:
                if consent.gender == MALE:
                    raise forms.ValidationError('You should fill the number of wives.')
            if husband_wives > 0:
                if consent.gender == FEMALE:
                    raise forms.ValidationError('You should fill the number of husband(s).')
            if not (husband_wives > 0 or num_wives > 0):
                raise forms.ValidationError(
                    'If participant is married, write the number of wives for the husband [WOMEN:] OR the number '
                    'of wives he is married to [MEN:].')
        return cleaned_data

    class Meta:
        model = Demographics
        fields = '__all__'
