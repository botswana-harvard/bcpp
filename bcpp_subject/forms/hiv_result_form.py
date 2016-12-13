from django import forms

from edc_constants.constants import NOT_APPLICABLE

from ..models import HivResult

from .form_mixins import SubjectModelFormMixin


class HivResultForm (SubjectModelFormMixin):

    def clean(self):

        cleaned_data = super(HivResultForm, self).clean()
        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = HivResult(**self.cleaned_data)
        # validating that hiv_result is not changed after HicEnrollment is filled.
        instance.hic_enrollment_checks(forms.ValidationError)
        # validating that a Microtube exists before filling this form.
        instance.microtube_checks(forms.ValidationError)
        # validating when testing declined
        if cleaned_data.get('hiv_result', None) == 'Declined' and not cleaned_data.get('why_not_tested', None):
            raise forms.ValidationError(
                'If participant has declined testing, provide reason participant declined testing')

        # validating when testing not performed
        if cleaned_data.get('hiv_result', None) == 'Not performed' and cleaned_data.get('why_not_tested', None):
            raise forms.ValidationError('If testing was not performed, DO NOT provide reason for declining')

        # testing declined but giving test date
        result_declined = (cleaned_data.get('hiv_result', None) == 'Declined')
        result_not_performed = (cleaned_data.get('hiv_result', None) == 'Not performed')
        if (result_declined or result_not_performed) and (cleaned_data.get('hiv_result_datetime', None)):
            raise forms.ValidationError(
                'If testing was declined or not performed, DO NOT give date and time of testing')

        # testing done but giving reason why not done
        if(
           (cleaned_data.get('hiv_result', None) == 'POS') or
           (cleaned_data.get('hiv_result', None) == 'NEG') or
           (cleaned_data.get('hiv_result', None) == 'IND')) and (cleaned_data.get('why_not_tested', None)):
            raise forms.ValidationError('If testing is performed, DO NOT provide reason for declining test')

        # testing done but not providing date
        if(
           (cleaned_data.get('hiv_result', None) == 'POS') or
           (cleaned_data.get('hiv_result', None) == 'NEG') or
           (cleaned_data.get('hiv_result', None) == 'IND')) and not (cleaned_data.get('hiv_result_datetime', None)):
            raise forms.ValidationError('If test has been performed, what is the test result date time?')
        self.validate_hiv_status_nd_blood_draw_type()
        if(
           cleaned_data.get('hiv_result') not in ['POS', 'NEG', 'IND'] and
           cleaned_data.get('insufficient_vol') in ['Yes', 'No']):
            raise forms.ValidationError(
                'No blood drawn.  You do not need to indicate if volume '
                'is sufficient. Got {0}'.format(cleaned_data.get('insufficient_vol')))
        if(
           cleaned_data.get('hiv_result') in ['POS', 'NEG', 'IND'] and
           cleaned_data.get('blood_draw_type') not in ['capillary', 'venous']):
            raise forms.ValidationError('Blood was drawn. Please indicate the type.')
        return cleaned_data

    def validate_hiv_status_nd_blood_draw_type(self):
        cleaned_data = self.cleaned_data
        if(
           cleaned_data.get('hiv_result') not in ['POS', 'NEG', 'IND'] and
           cleaned_data.get('blood_draw_type') in ['capillary', 'venous']):
            raise forms.ValidationError(
                'No blood drawn but you said {0}. Please correct.'.format(cleaned_data.get('blood_draw_type')))
        if(
           cleaned_data.get('blood_draw_type') == 'capillary' and
           cleaned_data.get('insufficient_vol') == NOT_APPLICABLE):
            raise forms.ValidationError('Please indicate if the capillary tube has sufficient volume.')
        if cleaned_data.get('blood_draw_type') == 'venous' and cleaned_data.get('insufficient_vol') in ['Yes', 'No']:
            raise forms.ValidationError(
                'Venous blood drawn.  You do not need to indicate if volume is '
                'sufficient. Got {0}'.format(cleaned_data.get('insufficient_vol')))

    class Meta:
        model = HivResult
        fields = '__all__'
