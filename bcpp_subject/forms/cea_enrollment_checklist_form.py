from django import forms

from ..models import CeaEnrollmentChecklist

from .form_mixins import SubjectModelFormMixin


class CeaEnrollmentChecklistForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = self.cleaned_data
        # If not a citizen, are they legall married to a Botswana citizen
        if cleaned_data.get('citizen') == 'No' and not cleaned_data.get('legal_marriage'):
            raise forms.ValidationError('if participant is not a citizen, is he/she married to a Botswana Citizen?')
        # if legally married, do they have a marriage certificate
        if cleaned_data.get('legal_marriage') == 'Yes' and not cleaned_data.get('marriage_certificate'):
            raise forms.ValidationError(
                'if participant is legally married to a Botswana Citizen, Where is the marriage certificate?')
        # if there is a certificate what is the marriage certificate number
        if cleaned_data.get('marriage_certificate') == 'Yes' and not cleaned_data.get('marriage_certificate_no'):
            raise forms.ValidationError(
                'if participant is legally married an has a marriage certificate, What is the marriage certificate no?')
        return cleaned_data

    class Meta:
        model = CeaEnrollmentChecklist
        fields = '__all__'
