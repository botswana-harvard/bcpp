from django import forms

from ..models import HivHealthCareCosts

from .form_mixins import SubjectModelFormMixin


class HivHealthCareCostsForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(HivHealthCareCostsForm, self).clean()

        if cleaned_data.get('hiv_medical_care') == 'Yes' and cleaned_data.get('reason_no_care') is not None:
            raise forms.ValidationError('If participant has received HIV medical care, reason '
                                        'for not receiving care should be None ')

        if cleaned_data.get('hiv_medical_care') == 'Yes' and not cleaned_data.get('place_care_received'):
            raise forms.ValidationError('If participant has received HIV medical care, '
                                        'where was it received? ')

        if cleaned_data.get('hiv_medical_care') == 'Yes' and cleaned_data.get('place_care_received') == 'None':
            raise forms.ValidationError('If participant has received HIV medical care, '
                                        'place where medical care received CANNOT be NONE? ')

        if cleaned_data.get('hiv_medical_care') == 'Yes' and not cleaned_data.get('care_regularity'):
            raise forms.ValidationError('If participant has received HIV medical care, how '
                                        'often was the care received? ')

        if cleaned_data.get('hiv_medical_care') == 'Yes' and not cleaned_data.get('doctor_visits'):
            raise forms.ValidationError('If participant has received HIV medical care, how '
                                        'often where you taken to see a doctor? ')

        if cleaned_data.get('hiv_medical_care') == 'No' and cleaned_data.get('place_care_received') != 'None':
            raise forms.ValidationError('If participant DID NOT received HIV medical care, then'
                                        'place care received should be NONE? ')

        return cleaned_data

    class Meta:
        model = HivHealthCareCosts
        fields = '__all__'
