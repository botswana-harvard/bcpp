from django import forms

from ..models import HivLinkageToCare, HivCareAdherence

from .form_mixins import SubjectModelFormMixin


class HivLinkageToCareForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(HivLinkageToCareForm, self).clean()
        instance = None
        subject_visit = None
        hiv_care_adherence = None
        if self.instance.id:
            instance = self.instance
            subject_visit = self.instance.subject_visit
        else:
            instance = HivLinkageToCare(**self.cleaned_data)
            subject_visit = instance.subject_visit
        try:
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=subject_visit)
        except HivCareAdherence.DoesNotExist:
            raise forms.ValidationError('Hiv Care Adherence has to be filled before filling this form.')
        if hiv_care_adherence.on_arv == 'Yes' and cleaned_data.get('startered_therapy', None) == 'No':
            raise forms.ValidationError(
                'If participant is said to be on art on the Hiv Care Adherence form this is contrary to the information given on question 12')
        if hiv_care_adherence.on_arv == 'No' and cleaned_data.get('startered_therapy', None) == 'Yes':
            raise forms.ValidationError(
                'If participant is said to be not on art on the Hiv Care Adherence form this is contrary to the information given on question 12')
        return cleaned_data

    class Meta:
        model = HivLinkageToCare
        fields = '__all__'
