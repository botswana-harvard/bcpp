from django import forms

from edc_constants.constants import YES, NO

from ..models import Education, SubjectLocator

from .form_mixins import SubjectModelFormMixin


class EducationForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(EducationForm, self).clean()
        # validating not working
        try:
            subject_locator = SubjectLocator.objects.get(subject_visit=cleaned_data.get('employed'))
            if subject_locator.may_call_work == YES and cleaned_data.get('working') == NO:
                raise forms.ValidationError(
                    'Participant gave permission to be contacted at WORK in the subject locator '
                    'but now reports to be \'Not Working\'. Either correct this form or change '
                    'answer in the Locator')
        except SubjectLocator.DoesNotExist:
            pass
        self.working_no()
        # retirement
        if cleaned_data.get('reason_unemployed') == 'retired' and not cleaned_data.get('monthly_income'):
            raise forms.ValidationError(
                'If participant is retired, how much of the retirement benefit is received monthly?')
        # student/apprentice/volunteer
        if cleaned_data.get('reason_unemployed') == 'student' and not cleaned_data.get('monthly_income'):
            raise forms.ValidationError(
                'If participant is student/apprentice/volunteer, how much payment is received monthly?')
        # validating for those employed
        self.working_yes()
        return cleaned_data

    def working_yes(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('working') == YES and cleaned_data.get('reason_unemployed'):
            raise forms.ValidationError(
                'You have provided unemployment details yet have indicated that participant is working')
        if cleaned_data.get('working') == YES and not cleaned_data.get('job_type'):
            raise forms.ValidationError('If participant is working, provide the job type')
        if cleaned_data.get('working') == YES and not cleaned_data.get('job_description'):
            raise forms.ValidationError('If participant is employed, what is the job description')
        if cleaned_data.get('working') == YES and not cleaned_data.get('monthly_income'):
            raise forms.ValidationError('If participant is employed, what is his/her monthly income?')

    def working_no(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('working') == NO and cleaned_data.get('job_type'):
            raise forms.ValidationError('If participant is not working, do not give job type')
        if cleaned_data.get('working') == NO and cleaned_data.get('job_description'):
            raise forms.ValidationError('Participant is not working, please do not provide any job description')
        # give reason for unemployment
        if cleaned_data.get('working') == NO and not cleaned_data.get('reason_unemployed'):
            raise forms.ValidationError('If participant is not working, provide reason for unemployment')

    class Meta:
        model = Education
        fields = '__all__'
