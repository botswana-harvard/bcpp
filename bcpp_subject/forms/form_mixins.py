from django import forms
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from edc_map.site_mappers import site_mappers

from survey.models import Survey

from ..models import SubjectVisit


class SubjectModelFormMixin(forms.ModelForm):

    visit_model = SubjectVisit

    def clean(self):
        cleaned_data = super(SubjectModelFormMixin, self).clean()
        self.limit_edit_to_current_community(cleaned_data)
        self.limit_edit_to_current_survey(cleaned_data)
        try:
            subject_visit = cleaned_data.get('subject_visit')
            if not subject_visit:
                subject_visit = self.instance.subject_visit
        except ObjectDoesNotExist:
            raise forms.ValidationError('Field Subject visit cannot be empty')
        report_datetime = cleaned_data.get('report_datetime')
        self.instance.consented_for_period_or_raise(
            report_datetime=report_datetime,
            subject_identifier=subject_visit.subject_identifier,
            exception_cls=forms.ValidationError)
        return cleaned_data

    def limit_edit_to_current_survey(self, cleaned_data):
        """Raises an exception if the instance does not refer to the
        current survey OR does nothing,"""
        try:
            if settings.LIMIT_EDIT_TO_CURRENT_SURVEY:
                current_survey = Survey.objects.current_survey()
                survey = cleaned_data.get('subject_visit').household_member.household_structure.survey
                if survey != current_survey:
                    raise forms.ValidationError(
                        'Form may not be saved. Only data from {} may be added/changed. '
                        '(LIMIT_EDIT_TO_CURRENT_SURVEY)'.format(current_survey))
        except AttributeError:
            pass
        return cleaned_data

    def limit_edit_to_current_community(self, cleaned_data):
        """Raises an exception if the instance does not refer to the
        current community OR does nothing,"""
        try:
            if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
                configured_community = site_mappers.get_mapper(site_mappers.current_map_area).map_area
                community = cleaned_data.get(
                    'subject_visit').household_member.household_structure.household.plot.community
                if community != configured_community:
                    raise forms.ValidationError(
                        'Form may not be saved. Only data from \'{}\' may be added/changed on '
                        'this device. Got {}. (LIMIT_EDIT_TO_CURRENT_COMMUNITY)'.format(
                            configured_community, community))
        except AttributeError:
            pass
        return cleaned_data
