from django import forms

from ..models import Pregnancy

from .form_mixins import SubjectModelFormMixin


class PregnancyForm (SubjectModelFormMixin):
    def clean(self):
        cleaned_data = super(PregnancyForm, self).clean()
        # pregnancy and antenatal registration
        if cleaned_data.get('current_pregnant') == 'Yes' and not cleaned_data.get('anc_reg'):
            raise forms.ValidationError('If participant currently pregnant, have they registered for antenatal care?')
        # if currently pregnant when was the last lnmp
        if cleaned_data.get('current_pregnant') == 'Yes' and not cleaned_data.get('lnmp'):
            raise forms.ValidationError('If participant currently pregnant, when was the last known menstrual period?')
        return cleaned_data

    class Meta:
        model = Pregnancy
        fields = '__all__'
