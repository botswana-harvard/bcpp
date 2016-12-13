from django import forms

from ..models import HivTested

from .form_mixins import SubjectModelFormMixin


class HivTestedForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(HivTestedForm, self).clean()
        if cleaned_data.get('num_hiv_tests') == 0:
            raise forms.ValidationError(
                'if participant has tested before, number of HIV tests before today cannot be zero. Please correct')
        # if no, don't answer next question
        if cleaned_data.get('hiv_pills') == 'No' and cleaned_data.get('arvs_hiv_test'):
            raise forms.ValidationError('You are answering information about ARV\'s yet have answered \'NO\', patient '
                                        'has never heard about ARV\'s. Please correct')
        # yes
        if cleaned_data.get('hiv_pills') == 'Yes' and not cleaned_data.get('arvs_hiv_test'):
            raise forms.ValidationError('if participant has heard about ARV\'s, provide information whether '
                                        'he/she believes that HIV positive can live longer if taking ARV\'s')
        # notsure
        if cleaned_data.get('hiv_pills') == 'not_sure' and not cleaned_data.get('arvs_hiv_test'):
            raise forms.ValidationError('Even if participant is not sure he/she heard about ARV\'s, provide '
                                        'information whether he/she believes that HIV positive can '
                                        'live longer if taking ARV\'s')
        return cleaned_data

    class Meta:
        model = HivTested
        fields = '__all__'
