from django import forms

from ..models import SubjectVisit
from ..models import SubjectConsent


class SubjectVisitForm (forms.ModelForm):

    def clean(self):
        cleaned_data = super(SubjectVisitForm, self).clean()
        subject_identifier = cleaned_data.get('household_member').get_subject_identifier()
        report_datetime = cleaned_data.get('report_datetime')
        self.instance.CONSENT_MODEL = SubjectConsent
        self.instance.consented_for_period_or_raise(
            report_datetime=report_datetime,
            subject_identifier=subject_identifier,
            exception_cls=forms.ValidationError)
        return cleaned_data

    class Meta:
        model = SubjectVisit
        fields = '__all__'
