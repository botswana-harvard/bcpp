from django import forms

from ..models import HicEnrollment

from .form_mixins import SubjectModelFormMixin


class HicEnrollmentForm (SubjectModelFormMixin):

    def clean(self):
        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = HicEnrollment(**self.cleaned_data)
        if not self.cleaned_data.get('hic_permission', None):
            raise forms.ValidationError('Provide an answer for whether participant gave permission for HIC.')
        if self.cleaned_data.get('hic_permission', None).lower() == 'yes':
            # Only enforce this criteria is subject enrols in HIC
            instance.is_permanent_resident(exception_cls=forms.ValidationError)
            instance.is_intended_residency(exception_cls=forms.ValidationError)
            instance.get_hiv_status_today(exception_cls=forms.ValidationError)
            instance.get_dob_consent_datetime(exception_cls=forms.ValidationError)
            instance.is_household_residency(exception_cls=forms.ValidationError)
            instance.is_citizen_or_spouse(exception_cls=forms.ValidationError)
            instance.is_locator_information(exception_cls=forms.ValidationError)
        return super(HicEnrollmentForm, self).clean()

    class Meta:
        model = HicEnrollment
        fields = '__all__'
