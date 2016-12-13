from datetime import date

from django import forms

from ..models import HivCareAdherence

from .form_mixins import SubjectModelFormMixin


class HivCareAdherenceForm (SubjectModelFormMixin):

    def clean(self):

        cleaned_data = super(HivCareAdherenceForm, self).clean()
        # if no medical care, explain why not
        if cleaned_data.get('medical_care', None) == 'No' and not cleaned_data.get('no_medical_care'):
            raise forms.ValidationError('If participant has not received any medical care, please give reason why not')
        if cleaned_data.get('why_no_arv', None) == 'Other' and not cleaned_data.get('why_no_arv_other'):
            raise forms.ValidationError(
                'If participant reason for not taking ARV\'s is \'OTHER\', specify reason why not started ARV\'s?')
        # if on_arv, need to answer clinic taking from and next scheduled appointment.
        self.validate_on_arv()
        self.validate_ever_taken_arv()
        if (cleaned_data.get('ever_recommended_arv', None) == 'Yes' and
                cleaned_data.get('ever_taken_arv', None) == 'No' and
                not cleaned_data.get('why_no_arv')):
            raise forms.ValidationError(
                'If participant has not taken any ARV\'s, give the main reason why not')
        # if currently taking arv's, how well has participant been taking medication
        if cleaned_data.get('arv_stop', None) == 'Other' and not cleaned_data.get('arv_stop_other'):
            raise forms.ValidationError(
                'If participant reason for stopping ARV\'s is \'OTHER\', '
                'specify reason why stopped taking ARV\'s?')

        # first HIV result cannot be received today
        if cleaned_data.get('first_positive'):
            if cleaned_data.get('first_positive') == date.today():
                raise forms.ValidationError(
                    'Date first received HIV positive result CANNOT be today. Please correct.')
        # confirming that evidence seen
        if cleaned_data.get('on_arv') == 'Yes' and not cleaned_data.get('arv_evidence'):
            raise forms.ValidationError(
                'If participant is on ARV, have you made this confirmation, seen any form of evidence?')
        # Validations for when participant is not on orv
        self.validate_not_on_art()
        if cleaned_data.get('next_appointment_date'):
            if not cleaned_data.get('next_appointment_date') >= date.today():
                raise forms.ValidationError(
                    'The next appointment date must be on or '
                    'after the report datetime. You entered '
                    '{0}'.format(cleaned_data.get('next_appointment_date').strftime('%Y-%m-%d')))

        return cleaned_data

    def validate_ever_taken_arv(self):
        cleaned_data = self.cleaned_data
        # if you are not currently on arv's you have to give the date you stopped taking arv
        if (cleaned_data.get('ever_taken_arv', None) == 'Yes' and
                cleaned_data.get('on_arv', None) == 'No' and not cleaned_data.get('arv_stop_date')):
            raise forms.ValidationError(
                'You have to indicate arv stop date if subject was on ARV and is NOT currently taking ARV\'s')
        # if partipant has taken arv's, give date when these were started
        if cleaned_data.get('ever_taken_arv', None) == 'Yes' and not cleaned_data.get('first_arv'):
            raise forms.ValidationError(
                'If participant has taken ARV\'s, give the date when these were first started.')
        # if participant has never taken ARV's, dont give a reason why they stopped.
        if cleaned_data.get('ever_taken_arv', None) == 'No' and cleaned_data.get('arv_stop'):
            raise forms.ValidationError(
                'If participant has NEVER taken ARV\'s, reason why they stopped should be \'None\'.')
        # if was recommended to take arv's but never taken arv's give reason why

        # if ARVs where taken in the past, then no need for reason why not started ARVS
        if cleaned_data.get('ever_taken_arv', None) == 'Yes' and cleaned_data.get('why_no_arv'):
            raise forms.ValidationError(
                'If participant has not taken ARV\'s in the past, DO NOT give '
                'the main reason why they have not started.')

    def validate_on_arv(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('on_arv', None) == 'Yes' and not cleaned_data.get('adherence_4_day'):
            raise forms.ValidationError('If participant is taking ARV\'s, have they skipped/ '
                                        'missed taking any? Please indicate')
        if cleaned_data.get('on_arv', None) == 'Yes':
            if (not cleaned_data.get('clinic_receiving_from', None) or
                    not cleaned_data.get('next_appointment_date', None)):
                raise forms.ValidationError(
                    'If patient is on ARV, provide the clinic facility and next scheduled appointment.')
        # if you are not taking any arv's do not indicate that you have missed taking medication
        if cleaned_data.get('on_arv', None) == 'No' and cleaned_data.get('adherence_4_day'):
            raise forms.ValidationError(
                'You do not have to indicate missed medication because you are not taking any ARV\'s')
        # if you are currently on arv's do not give the date or reason you stopped taking arv
        if (cleaned_data.get('on_arv', None) == 'Yes' and
                (cleaned_data.get('arv_stop_date') or cleaned_data.get('arv_stop'))):
            raise forms.ValidationError(
                'Do not indicate arv STOP DATE or STOP REASON if subject is currently taking ARV\'s')

        if cleaned_data.get('on_arv', None) == 'Yes' and not cleaned_data.get('adherence_4_wk'):
            raise forms.ValidationError(
                'If participant is currently taking ARV\'s, how well has he/she been '
                'taking the medication this past week?')

    def validate_not_on_art(self):
        cleaned_data = self.cleaned_data
        # Particpants that reports to have never taken ARV's cannot be on ARV's now.
        if cleaned_data.get('ever_taken_arv', None) == 'No' and cleaned_data.get('on_arv', None) == 'Yes':
            raise forms.ValidationError('Particpants that reports to have never taken ARV\'s cannot be on ARV\'s now.')
        if cleaned_data.get('on_arv', None) == 'No':
            if cleaned_data.get('clinic_receiving_from', None) or cleaned_data.get('next_appointment_date', None):
                raise forms.ValidationError(
                    'If patient is NOT ARV, DO NOT provide the clinic facility and next scheduled appointment.')

            if (cleaned_data.get('ever_taken_arv', None) == 'No' and
                    (cleaned_data.get('arv_stop_date', None) or
                     cleaned_data.get('arv_stop_other', None) or cleaned_data.get('arv_stop', None))):
                raise forms.ValidationError(
                    'If patient is was NEVER ON ARV, DO NOT provide the stop date and reason for stopping.')
            if cleaned_data.get('adherence_4_wk', None) or cleaned_data.get('adherence_4_day', None):
                raise forms.ValidationError('If patient is NOT ARV, DO NOT provide any adherance information.')

    class Meta:
        model = HivCareAdherence
        fields = '__all__'
