from django import forms

from ..constants import ANNUAL
from ..models import MedicalDiagnoses

from .form_mixins import SubjectModelFormMixin


class MedicalDiagnosesForm (SubjectModelFormMixin):

    optional_labels = {
        ANNUAL: {'diagnoses': (
            'Since we spoke with you at our last visit, do you recall or is there a record '
            'of having any of the following serious illnesses?'),
        }
    }

    def clean(self):
        cleaned_data = super(MedicalDiagnosesForm, self).clean()
        diagnoses_list = []
        if not cleaned_data.get('diagnoses', None):
            raise forms.ValidationError('You have to provide a previous diagnoses, otherwise \'None\'.')

        for diagnoses in cleaned_data.get('diagnoses'):
            diagnoses_list.append(diagnoses.name)

        if 'None' in diagnoses_list and len(cleaned_data.get('diagnoses')) > 1:
            raise forms.ValidationError('The diagnosis can not be None and other diagnosis at the same time.')
        # heart_attack
        if 'Heart Disease or Stroke' in diagnoses_list and not cleaned_data.get('heart_attack_record'):
            raise forms.ValidationError('If participant has ever had a heart attack, is there a record available?')
        # cancer
        if 'Cancer' in diagnoses_list and not cleaned_data.get('cancer_record'):
            raise forms.ValidationError(
                'If participant has ever been diagnosed with cancer, is there a record available?')
        # TB
        if 'Tubercolosis' in diagnoses_list and not cleaned_data.get('tb_record'):
            raise forms.ValidationError('If participant has ever been diagnosed with TB, is there a record available?')
        if(
           (cleaned_data.get('heart_attack_record') and 'Heart Disease or Stroke' not in diagnoses_list) or
           (cleaned_data.get('cancer_record') and 'Cancer' not in diagnoses_list) or
           (cleaned_data.get('tb_record') and 'Tubercolosis' not in diagnoses_list)):
            raise forms.ValidationError('You cannot enter a record for a diagnosis you did not specify')
        if(
           'None' in diagnoses_list and (cleaned_data.get('heart_attack_record') or
                                         cleaned_data.get('cancer_record') or cleaned_data.get('tb_record'))):
            raise forms.ValidationError('If the diagnosis is None, then all \'records\' have to be None')

        return cleaned_data

    class Meta:
        model = MedicalDiagnoses
        fields = '__all__'
