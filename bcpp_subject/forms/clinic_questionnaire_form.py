from django import forms

from ..models import ClinicQuestionnaire

from .form_mixins import SubjectModelFormMixin


class ClinicQuestionnaireForm (SubjectModelFormMixin):
    def clean(self):

        cleaned_data = super(ClinicQuestionnaireForm, self).clean()

        # if knowing HIV status
        if cleaned_data.get('know_hiv_status', None) == 'Yes' and not cleaned_data.get('current_hiv_status'):
            raise forms.ValidationError(
                'If participant knows their HIV status, ask the participant to tell you the current HIV status')
        # if POS, on ARV?
        if cleaned_data.get('current_hiv_status', None) == 'POS' and not cleaned_data.get('on_arv'):
            raise forms.ValidationError('If participant is HIV positive, is participant on ARV therapy?')
        # if on ARV, is there evidence
        if cleaned_data.get('on_arv', None) == 'Yes' and not cleaned_data.get('arv_evidence'):
            raise forms.ValidationError(
                'If participant is on ARV, is there evidence of being on therapy [OPD card, tablets, masa number]?')
        # NO
        if (
            cleaned_data.get('know_hiv_status', None) == 'No' and
            (cleaned_data.get('current_hiv_status') or
             cleaned_data.get('on_arv') or cleaned_data.get('arv_evidence'))
        ):
            raise forms.ValidationError(
                'If participant does not know their HIV status, do not provide any other details')

        return cleaned_data

    class Meta:
        model = ClinicQuestionnaire
        fields = '__all__'
