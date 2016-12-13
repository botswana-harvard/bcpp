from django import forms

from ..models import Cd4History

from .form_mixins import SubjectModelFormMixin


class Cd4HistoryForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(Cd4HistoryForm, self).clean()
        if (
            cleaned_data.get('record_available') == 'Yes' and not cleaned_data.get('last_cd4_count') and not
            cleaned_data.get('last_cd4_drawn_date')
        ):
            raise forms.ValidationError(
                'If last known record of CD4 count is available or known, please '
                'provide the CD4 count and the CD4 date')
        if (
            cleaned_data.get('record_available') == 'No' and
            (cleaned_data.get('last_cd4_count', None) or cleaned_data.get('last_cd4_drawn_date', None))
        ):
            raise forms.ValidationError(
                'If last known record of CD4 count is not available or not known, please do NOT'
                ' provide the CD4 count and the CD4 date')
        return cleaned_data

    class Meta:
        model = Cd4History
        fields = '__all__'
