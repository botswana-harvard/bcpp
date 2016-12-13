from django import forms

from ..models import SubjectReferral
from ..subject_referral_helper import SubjectReferralHelper

from .form_mixins import SubjectModelFormMixin


class SubjectReferralForm(SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(SubjectReferralForm, self).clean()
        subject_referral_helper = SubjectReferralHelper(SubjectReferral(**cleaned_data))
        if subject_referral_helper.missing_data:
            raise forms.ValidationError(
                'Some data is missing for the referral. Complete \'{0}\' first '
                'and try again.'.format(subject_referral_helper.missing_data._meta.verbose_name))
        return cleaned_data

    class Meta:
        model = SubjectReferral
        fields = '__all__'
