from django import forms

from ..models import Participation

from .form_mixins import SubjectModelFormMixin


class ParticipationForm (SubjectModelFormMixin):
    def clean(self):

        cleaned_data = super(ParticipationForm, self).clean()
        if cleaned_data.get('full') == 'No' and cleaned_data.get('participation_type') == 'Not Applicable':
            raise forms.ValidationError(
                'Participation type cannot be \'Not Applicable\' if participant is not fully participating in BHS.')
        if cleaned_data.get('full') == 'Yes' and cleaned_data.get('participation_type') != 'Not Applicable':
            raise forms.ValidationError(
                'If full participation is chosen, type of participation should be \'Not Applicable\'.')

        return cleaned_data

    class Meta:
        model = Participation
        fields = '__all__'
