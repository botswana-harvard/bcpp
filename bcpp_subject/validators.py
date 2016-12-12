from datetime import datetime, time

from django.core.exceptions import ValidationError

from edc_map.site_mappers import site_mappers

from bcpp_survey.models import Survey


def date_in_survey(value):
    if not value:
        pass
    else:
        value_datetime = datetime.combine(value, time.min)
        current_survey = Survey.objects.current_survey(report_datetime=value_datetime)
        mapper = site_mappers.get_mapper(site_mappers.current_community)
        start_date = mapper.survey_dates.get(current_survey.survey_slug).start_date
        end_date = mapper.survey_dates.get(current_survey.survey_slug).end_date
        if value < start_date or value > end_date:
            raise ValidationError('Appointment must fall within survey {} (from {} to {}). You entered {}'.format(
                current_survey.survey_slug, start_date, end_date, value,))
