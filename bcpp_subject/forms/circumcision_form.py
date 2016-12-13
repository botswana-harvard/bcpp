from django import forms

from ..constants import ANNUAL
from ..models import Circumcision, Uncircumcised, Circumcised

from .form_mixins import SubjectModelFormMixin


class CircumcisionForm (SubjectModelFormMixin):

    optional_labels = {
        ANNUAL: {'circumcised': (
            'Have you been circumcised since we last spoke with you?'),
        }
    }

    class Meta:
        model = Circumcision
        fields = '__all__'


class CircumcisedForm (SubjectModelFormMixin):

    def clean(self):

        cleaned_data = super(CircumcisedForm, self).clean()
        if cleaned_data.get('circumcised') == 'Yes' and not cleaned_data.get('health_benefits_smc'):
            raise forms.ValidationError('if \'YES\', what are the benefits of male circumcision?.')
        if cleaned_data.get('when_circ') and not cleaned_data.get('age_unit_circ'):
            raise forms.ValidationError('If you answered age of circumcision then you must provide time units.')
        if not cleaned_data.get('when_circ') and cleaned_data.get('age_unit_circ'):
            raise forms.ValidationError(
                'If you did not answer age of circumcision then you must not provide time units.')
        return cleaned_data

    class Meta:
        model = Circumcised
        fields = '__all__'


class UncircumcisedForm (SubjectModelFormMixin):
    def clean(self):

        cleaned_data = super(UncircumcisedForm, self).clean()
        if cleaned_data.get('circumcised') == 'Yes' and not cleaned_data.get('health_benefits_smc'):
            raise forms.ValidationError('if \'YES\', what are the benefits of male circumcision?.')
        return cleaned_data

    class Meta:
        model = Uncircumcised
        fields = '__all__'
