from django import forms

from ..models import ElisaHivResult

from .form_mixins import SubjectModelFormMixin


class ElisaHivResultForm (SubjectModelFormMixin):

    def clean(self):

        cleaned_data = super(ElisaHivResultForm, self).clean()
        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = ElisaHivResult(**self.cleaned_data)
        # validating that hiv_result is not changed after HicEnrollment is filled.
        instance.hic_enrollment_checks(forms.ValidationError)
        # validating that a Microtube exists before filling this form.
        instance.elisa_requisition_checks(forms.ValidationError)

        # testing done but not providing date
        if(
           ((cleaned_data.get('hiv_result', None) == 'POS') or (cleaned_data.get('hiv_result', None) == 'NEG')) and not
           cleaned_data.get('hiv_result_datetime', None)):
            raise forms.ValidationError('If test has been performed, what is the test result date time?')

        return cleaned_data

    class Meta:
        model = ElisaHivResult
        fields = '__all__'
