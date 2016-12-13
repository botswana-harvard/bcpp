from django import forms

from ..models import OutpatientCare

from .form_mixins import SubjectModelFormMixin


class OutpatientCareForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(OutpatientCareForm, self).clean()

        if cleaned_data.get('govt_health_care') == 'Yes' and not cleaned_data.get('care_visits'):
            raise forms.ValidationError('If participant seeked care from Govt, how many outpatient '
                                        'visits were there?')

        if (cleaned_data.get('govt_health_care') == 'Yes' and
                cleaned_data.get('facility_visited') == 'No visit in past 3 months'):
            raise forms.ValidationError('If participant seeked care from Govt, answer about '
                                        'facility CANNOT be NO VISIT?')

        if cleaned_data.get('govt_health_care') == 'Yes' and not cleaned_data.get('care_reason'):
            raise forms.ValidationError('If participant seeked care from Govt, what was the '
                                        'primary reason for seeking care?')
        if cleaned_data.get('govt_health_care') == 'Yes' and cleaned_data.get('care_reason') == 'None':
            raise forms.ValidationError('If participant has seeked care, reason for receiving '
                                        'CANNOT be NONE?')
        if cleaned_data.get('govt_health_care') == 'Yes' and cleaned_data.get('outpatient_expense') is None:
            raise forms.ValidationError('If participant seeked care from Govt, how much did he/she '
                                        'have to pay the health care provider?')
        if cleaned_data.get('govt_health_care') == 'Yes' and not cleaned_data.get('travel_time'):
            raise forms.ValidationError('how long did it take you to get to the clinic/hospital?')
        if cleaned_data.get('govt_health_care') == 'Yes' and cleaned_data.get('waiting_hours') == 'None':
            raise forms.ValidationError('If participant has seeked care, waiting hours to be '
                                        'seen cannot be None')
        return cleaned_data

    class Meta:
        model = OutpatientCare
        fields = '__all__'
