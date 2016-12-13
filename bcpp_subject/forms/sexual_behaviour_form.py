from django import forms

from ..models import SexualBehaviour

from .form_mixins import SubjectModelFormMixin

from ..constants import ANNUAL


class SexualBehaviourForm (SubjectModelFormMixin):

    optional_attrs = {ANNUAL: {
        'label': {
            'last_year_partners': (
                'Since we spoke with you at our last visit, how many different people have you had '
                'sex with? Please remember to include '
                'casual and once-off partners (prostitutes and truck drivers) as well as long-term '
                'partners (spouses, boyfriends/girlfriends)[If you can\'t recall the exact number, '
                'please give a best guess]'),
            'more_sex': (
                'Since we spoke with you at our last visit, did you have sex with '
                'somebody living outside of the community? '),
        }
    }}

    def clean(self):
        cleaned_data = super(SexualBehaviourForm, self).clean()
        # validating no sex
        self.validate_no_sex('lifetime_sex_partners', cleaned_data)
        self.validate_no_sex('last_year_partners', cleaned_data)
        self.validate_no_sex('more_sex', cleaned_data)
        self.validate_no_sex('first_sex', cleaned_data)
        self.validate_no_sex('condom', cleaned_data)
        self.validate_no_sex('alcohol_sex', cleaned_data)

        # ensuring that the number of last year partners is not greater than lifetime partners
        if cleaned_data.get('ever_sex') == 'Yes':
            if not cleaned_data.get('lifetime_sex_partners'):
                raise forms.ValidationError('If participant has ever had sex, CANNOT have 0 lifetime partners.')

        if cleaned_data.get('more_sex') == 'Yes':
            if not cleaned_data.get('last_year_partners'):
                raise forms.ValidationError(
                    'If participant has ever had sex with somebody living outside of the '
                    'community, CANNOT have 0 last year partners.')

        # If number of sexual partners in past 12months is more than zero, did
        # participant have sex with anyone outside the community 12months ago
        if cleaned_data.get('last_year_partners') > 0 and not cleaned_data.get('more_sex'):
            raise forms.ValidationError(
                'If participant has had sex with anyone in the past 12months, has participant '
                'had sex with anyone outside community in the past 12months?')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('condom'):
            raise forms.ValidationError(
                'If participant has had sex at some point in their life, did participant '
                'use a condom the last time he/she had sex?')
        if cleaned_data.get('ever_sex') == 'Yes' and not cleaned_data.get('alcohol_sex'):
            raise forms.ValidationError(
                'If participant has had sex at some point in their life, did participant '
                'drink alcohol before sex last time?')

        if cleaned_data.get('last_year_partners') > cleaned_data.get('lifetime_sex_partners'):
            raise forms.ValidationError(
                'Number of partners in the past 12months CANNOT exceed number of life time partners')
        return cleaned_data

    def validate_no_sex(self, field, cleaned_data):
        msg = 'If participant has NEVER had sex, DO NOT provide any other sexual intercourse related questions'
        self.validate_dependent_fields('ever_sex', field, cleaned_data, msg)

    def validate_dependent_fields(self, master_field, sub_field, cleaned_data, msg):
        if cleaned_data.get(master_field, None) == 'No' and cleaned_data.get(sub_field, None):
            raise forms.ValidationError(msg)

    class Meta:
        model = SexualBehaviour
        fields = '__all__'
