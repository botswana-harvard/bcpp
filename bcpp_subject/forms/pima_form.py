from django import forms

from ..models import Pima

from .form_mixins import SubjectModelFormMixin


class PimaForm (SubjectModelFormMixin):

    def clean(self):

        cleaned_data = super(PimaForm, self).clean()
        if cleaned_data.get('pima_today') == 'No' and not cleaned_data.get('pima_today_other'):
            raise forms.ValidationError('If PIMA CD4 NOT done today, please explain why not?')

        # If no PIMA CD4 performed, do not provide any CD4 related information
        if cleaned_data.get('pima_today') == 'No' and cleaned_data.get('pima_id'):
            raise forms.ValidationError('Do not provide the PIMA machine id if the PIMA CD4 was not performed')
        if cleaned_data.get('pima_today') == 'No' and cleaned_data.get('cd4_value'):
            raise forms.ValidationError('PIMA CD4 was not performed, do not provide the CD4 value')

        # If PIMA CD4 performed, provide details
        if cleaned_data.get('pima_today') == 'Yes' and not cleaned_data.get('pima_id'):
            raise forms.ValidationError('If PIMA CD4 done today, please provide machine id?')
        if cleaned_data.get('pima_today') == 'Yes' and not cleaned_data.get('cd4_value'):
            raise forms.ValidationError('If PIMA CD4 done today, what is the CD4 value?')
        if cleaned_data.get('pima_today') == 'Yes' and not cleaned_data.get('cd4_datetime'):
            raise forms.ValidationError('If PIMA CD4 done today, what is the CD4 test datetime?')

        return cleaned_data

    class Meta:
        model = Pima
        fields = '__all__'
