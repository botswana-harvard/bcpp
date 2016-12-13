from django import forms
from datetime import date

from ..models import HivTestReview, HivTestingHistory

from .form_mixins import SubjectModelFormMixin


class HivTestReviewForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(HivTestReviewForm, self).clean()
        return cleaned_data

    def clean_hiv_test_date(self):
        hiv_test_date = self.cleaned_data.get('hiv_test_date')
        if hiv_test_date:
            if hiv_test_date == date.today():
                raise forms.ValidationError('The HIV test date cannot be equal to today\'s date. Please correct.')
        return hiv_test_date

    class Meta:
        model = HivTestReview
        fields = '__all__'
