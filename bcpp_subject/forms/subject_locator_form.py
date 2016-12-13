from django import forms
from edc_constants.choices import NOT_APPLICABLE

from ..models import SubjectLocator

from .form_mixins import SubjectModelFormMixin


class SubjectLocatorForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(SubjectLocatorForm, self).clean()
        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = SubjectLocator(**self.cleaned_data)
        # validating that some contact numbers exist when HicEnrollment form exists.
        instance.hic_enrollment_checks(forms.ValidationError)
        # validating home_visits
        if cleaned_data.get('home_visit_permission', None) == 'No' and cleaned_data.get('physical_address', None):
            raise forms.ValidationError(
                'If participant has not given permission to make'
                ' home_visits, do not give physical(home) address details')
        # requiring info to be keyed
        # home_visit permission
        if cleaned_data.get('home_visit_permission', None) == 'Yes' and not cleaned_data.get('physical_address', None):
            raise forms.ValidationError(
                'If participant has allowed you to make home visits, what is their physical address?')
        # permission to followup
        if cleaned_data.get('may_follow_up', None) == 'Yes' and not cleaned_data.get('subject_cell', None):
            raise forms.ValidationError('If participant has allowed you to follow them up, what is their cell number?')
        # permission to sms
        if cleaned_data.get('may_sms_follow_up', None) == 'Yes' and not cleaned_data.get('subject_cell', None):
            raise forms.ValidationError(
                'If participant has allowed you to sms her on followup, what is their cell number?')
        # may call work
        self.validate_may_call_work_yes()
        # Contact next-of-kin
        if(
           cleaned_data.get('may_contact_someone', None) == 'No' and not
           cleaned_data.get('has_alt_contact', None) == NOT_APPLICABLE):
            raise forms.ValidationError(
                'If participant has answered No to question 12 then question 19 is Not Applicable')
        if cleaned_data.get('has_alt_contact', None) == 'Yes' and not cleaned_data.get('alt_contact_name', None):
            raise forms.ValidationError(
                'If participant has allowed you to contact next-of-kin, what is their full name?')
        if cleaned_data.get('has_alt_contact', None) == 'Yes' and not cleaned_data.get('alt_contact_rel', None):
            raise forms.ValidationError('If participant has allowed you to contact next-of-kin, how are they related?')
        # may contact someone else
        self.validate_may_contact_someone_yes()
        # validating work_place
        self.validate_work_place('subject_work_place', cleaned_data)
        self.validate_work_place('subject_work_phone', cleaned_data)
        # validating follow_up
        self.validate_call_sms_follow_up('subject_cell', cleaned_data)
        self.validate_call_sms_follow_up('subject_cell_alt', cleaned_data)
        self.validate_call_follow_up('subject_phone', cleaned_data)
        self.validate_call_follow_up('subject_phone_alt', cleaned_data)
        # validating next_of_kin
        self.validate_next_of_kin('alt_contact_name', cleaned_data)
        self.validate_next_of_kin('alt_contact_rel', cleaned_data)
        self.validate_next_of_kin('alt_contact_cell', cleaned_data)
        self.validate_next_of_kin('other_alt_contact_cell', cleaned_data)
        self.validate_next_of_kin('alt_contact_tel', cleaned_data)
        # validating anyone_else contact
        self.validate_contact_someone('contact_name', cleaned_data)
        self.validate_contact_someone('contact_rel', cleaned_data)
        self.validate_contact_someone('contact_physical_address', cleaned_data)
        self.validate_contact_someone('contact_cell', cleaned_data)
        self.validate_contact_someone('contact_phone', cleaned_data)

        return cleaned_data

    def validate_may_call_work_yes(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('may_call_work', None) == 'Yes' and not cleaned_data.get('subject_work_place', None):
            raise forms.ValidationError(
                'If participant has allowed you to call them at work, name work place location?')
        if cleaned_data.get('may_call_work', None) == 'Yes' and not cleaned_data.get('subject_work_phone', None):
            raise forms.ValidationError(
                'If participant has allowed you to call them at work, give the work phone number?')

    def validate_may_contact_someone_yes(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('may_contact_someone', None) == 'Yes' and not cleaned_data.get('contact_name', None):
            raise forms.ValidationError(
                'If participant has allowed you to contact someone else, what is the contact name?')
        if cleaned_data.get('may_contact_someone', None) == 'Yes' and not cleaned_data.get('contact_rel', None):
            raise forms.ValidationError(
                'If participant has allowed you to contact someone else, how are they related to this person?')
        if(
           cleaned_data.get('may_contact_someone', None) == 'Yes' and not
           cleaned_data.get('contact_physical_address', None)):
            raise forms.ValidationError(
                'If participant has allowed you to contact someone else, what is this persons physical address?')

    def validate_call_follow_up(self, field, cleaned_data):
        msg = 'If participant has not given permission for follow-up, do not give follow-up details'
        self.validate_dependent_fields(['may_follow_up', 'may_sms_follow_up'], field, cleaned_data, msg)

    def validate_call_sms_follow_up(self, field, cleaned_data):
        msg = 'If participant has not given permission for follow-up, do not give follow-up details'
        self.validate_dependent_fields(['may_follow_up', 'may_sms_follow_up'], field, cleaned_data, msg)

    def validate_next_of_kin(self, field, cleaned_data):
        msg = 'If participant has not given permission to contact next_of_kin, do not give next_of_kin details'
        self.validate_dependent_fields(['has_alt_contact'], field, cleaned_data, msg)

    def validate_work_place(self, field, cleaned_data):
        msg = 'If participant has not given permission to contact him/her at work, do not give work details'
        self.validate_dependent_fields(['may_call_work'], field, cleaned_data, msg)

    def validate_contact_someone(self, field, cleaned_data):
        msg = 'If participant has not given permission to contact anyone else for follow up purposes, '
        'do not give any other details'
        self.validate_dependent_fields(['may_contact_someone'], field, cleaned_data, msg)

    def validate_dependent_fields(self, master_fields, sub_field, cleaned_data, msg):
        permitted = False
        for field in master_fields:
            if cleaned_data.get(field, None) == 'Yes':
                permitted = True
        if not permitted and cleaned_data.get(sub_field, None):
            raise forms.ValidationError(msg)

    def limit_edit_to_current_survey(self, cleaned_data):
        return cleaned_data

    class Meta:
        model = SubjectLocator
        fields = '__all__'
