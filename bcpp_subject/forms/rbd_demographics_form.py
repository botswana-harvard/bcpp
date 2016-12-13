from django import forms

from ..models import RbdDemographics

from .form_mixins import SubjectModelFormMixin


class RbdDemographicsForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(RbdDemographicsForm, self).clean()

        # validating unmarried
        if cleaned_data.get('marital_status', None) != 'Married' and cleaned_data.get('num_wives', None):
            raise forms.ValidationError('If participant is not married, do not give number of wives')
        if cleaned_data.get('marital_status', None) != 'Married' and cleaned_data.get('husband_wives', None):
            raise forms.ValidationError('If participant is not married, the number of wives is not required')

        # validating if married
        if cleaned_data.get('marital_status') == 'Married':
            husband_wives = cleaned_data.get('husband_wives', 0)
            num_wives = cleaned_data.get('num_wives', 0)
            if husband_wives > 0 and num_wives > 0:
                raise forms.ValidationError('You CANNOT fill in both for WOMEN & MEN. Choose one')
            if not (husband_wives > 0 or num_wives > 0):
                raise forms.ValidationError(
                    'If participant is married, write the number of wives for the husband [WOMEN:] OR the number of '
                    'wives he is married to [MEN:].')

        return cleaned_data

    class Meta:
        model = RbdDemographics
        fields = '__all__'
