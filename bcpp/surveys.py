# coding=utf-8
import arrow

from datetime import datetime
from dateutil.tz import gettz

from django.conf import settings

from survey import site_surveys, Survey, SurveySchedule

from .communities import communities
from django.core.exceptions import ImproperlyConfigured

if settings.CURRENT_MAP_AREA not in communities:
    raise ImproperlyConfigured(
        f'Current map area \'{settings.CURRENT_MAP_AREA}\' not in dictionary of communities.')

tzinfo = gettz(settings.TIME_ZONE)

ANONYMOUS_SURVEY = 'ano'
ESS_SURVEY = 'ess'
AHS_SURVEY = 'ahs'
BHS_SURVEY = 'bhs'
BCPP_YEAR_1 = 'bcpp-year-1'
BCPP_YEAR_2 = 'bcpp-year-2'
BCPP_YEAR_3 = 'bcpp-year-3'

bcpp_year_one = SurveySchedule(
    name=BCPP_YEAR_1,
    group_name=settings.SURVEY_GROUP_NAME,
    map_areas=communities,
    start=arrow.get(
        datetime(2013, 10, 18, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2015, 1, 31, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime)

bcpp_year_two = SurveySchedule(
    name=BCPP_YEAR_2,
    group_name=settings.SURVEY_GROUP_NAME,
    map_areas=communities,
    start=arrow.get(
        datetime(2015, 2, 1, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2016, 12, 15, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime)

bcpp_year_three = SurveySchedule(
    name=BCPP_YEAR_3,
    group_name=settings.SURVEY_GROUP_NAME,
    map_areas=communities,
    start=arrow.get(
        datetime(2017, 1, 26, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2018, 4, 9, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime)

# year 1 surveys
bcpp_year_one.add_survey(
    Survey(
        name=BHS_SURVEY,
        position=0,
        map_area=settings.CURRENT_MAP_AREA,
        start=bcpp_year_one.start,
        end=bcpp_year_one.end,
        full_enrollment_datetime=bcpp_year_one.end)
)


# year 2 surveys
bcpp_year_two.add_survey(
    Survey(
        name=BHS_SURVEY,
        position=0,
        map_area=settings.CURRENT_MAP_AREA,
        start=bcpp_year_two.start,
        end=bcpp_year_two.end,
        full_enrollment_datetime=bcpp_year_two.end)
)

bcpp_year_two.add_survey(
    Survey(
        name=AHS_SURVEY,
        position=1,
        map_area=settings.CURRENT_MAP_AREA,
        start=bcpp_year_two.start,
        end=bcpp_year_two.end,
        full_enrollment_datetime=bcpp_year_two.end)
)

# year 3 surveys
bcpp_year_three.add_survey(
    Survey(
        name=AHS_SURVEY,
        position=0,
        map_area=settings.CURRENT_MAP_AREA,
        start=bcpp_year_three.start,
        end=bcpp_year_three.end,
        full_enrollment_datetime=bcpp_year_three.end)
)

bcpp_year_three.add_survey(
    Survey(
        name=ESS_SURVEY,
        position=1,
        map_area=settings.CURRENT_MAP_AREA,
        start=bcpp_year_three.start,
        end=bcpp_year_three.end,
        full_enrollment_datetime=bcpp_year_three.end)
)

bcpp_year_three.add_survey(
    Survey(
        name=ANONYMOUS_SURVEY,
        position=0,
        map_area=settings.CURRENT_MAP_AREA,
        start=bcpp_year_three.start,
        end=bcpp_year_three.end,
        full_enrollment_datetime=bcpp_year_three.end)
)


site_surveys.register(bcpp_year_one)
site_surveys.register(bcpp_year_two)
site_surveys.register(bcpp_year_three)
