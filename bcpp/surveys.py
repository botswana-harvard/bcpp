# coding=utf-8
import arrow

from datetime import datetime
from dateutil.tz import gettz

from survey import site_surveys, Survey, SurveySchedule

from .communities import communities

tzinfo = gettz('Africa/Gaborone')

ANONYMOUS_SURVEY = 'ano'
ESS_SURVEY = 'ess'
AHS_SURVEY = 'ahs'
BHS_SURVEY = 'bhs'
BCPP_YEAR_1 = 'bcpp-year-1'
BCPP_YEAR_2 = 'bcpp-year-2'
BCPP_YEAR_3 = 'bcpp-year-3'

bcpp_year_one = SurveySchedule(
    name=BCPP_YEAR_1,
    group_name='bcpp-survey',
    map_areas=communities,
    start=arrow.get(
        datetime(2013, 10, 18, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2015, 1, 31, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime)

bcpp_year_two = SurveySchedule(
    name=BCPP_YEAR_2,
    group_name='bcpp-survey',
    map_areas=communities,
    start=arrow.get(
        datetime(2015, 2, 1, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2016, 12, 15, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime)

bcpp_year_three = SurveySchedule(
    name=BCPP_YEAR_3,
    group_name='bcpp-survey',
    map_areas=communities,
    start=arrow.get(
        datetime(2017, 2, 1, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2018, 4, 9, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime)

# year 1 surveys
bhs_survey_y1 = Survey(
    name=BHS_SURVEY,
    position=0,
    map_area='test_community',
    start=bcpp_year_one.start,
    end=bcpp_year_one.end,
    full_enrollment_datetime=bcpp_year_one.end,
)

bcpp_year_one.add_survey(bhs_survey_y1)


# year 2 surveys
bhs_survey_y2 = Survey(
    name=BHS_SURVEY,
    position=0,
    map_area='test_community',
    start=bcpp_year_two.start,
    end=bcpp_year_two.end,
    full_enrollment_datetime=bcpp_year_two.end,
)

ahs_survey_y2 = Survey(
    name=AHS_SURVEY,
    position=1,
    map_area='test_community',
    start=bcpp_year_two.start,
    end=bcpp_year_two.end,
    full_enrollment_datetime=bcpp_year_two.end,
)
bcpp_year_two.add_survey(bhs_survey_y2, ahs_survey_y2)

# year 3 surveys
ahs_survey_y3 = Survey(
    name=AHS_SURVEY,
    position=0,
    map_area='test_community',
    start=bcpp_year_three.start,
    end=bcpp_year_three.end,
    full_enrollment_datetime=bcpp_year_three.end,
)
ess_survey_y3 = Survey(
    name=ESS_SURVEY,
    position=1,
    map_area='test_community',
    start=bcpp_year_three.start,
    end=bcpp_year_three.end,
    full_enrollment_datetime=bcpp_year_three.end,
)
ano_survey_y3 = Survey(
    name=ANONYMOUS_SURVEY,
    position=1,
    map_area='test_community',
    start=bcpp_year_three.start,
    end=bcpp_year_three.end,
    full_enrollment_datetime=bcpp_year_three.end,
)

bcpp_year_three.add_survey(ahs_survey_y3, ess_survey_y3, ano_survey_y3)

site_surveys.register(bcpp_year_one)
site_surveys.register(bcpp_year_two)
site_surveys.register(bcpp_year_three)
