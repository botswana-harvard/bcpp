# coding=utf-8

from dateutil.relativedelta import relativedelta

from edc_base.utils import get_utcnow

from survey.site_surveys import site_surveys
from survey.survey import Survey
from survey.survey_schedule import SurveySchedule


bcpp_year_one = SurveySchedule(
    name='bcpp-year-1',
    group_name='bcpp-survey',
    start_date=(get_utcnow() - relativedelta(years=3)).date(),
    end_date=(get_utcnow() - relativedelta(years=2)).date())

bcpp_year_two = SurveySchedule(
    name='bcpp-year-2',
    group_name='bcpp-survey',
    start_date=(get_utcnow() - relativedelta(years=2)).date(),
    end_date=(get_utcnow() - relativedelta(years=1)).date())

bcpp_year_three = SurveySchedule(
    name='bcpp-year-3',
    group_name='bcpp-survey',
    start_date=(get_utcnow() - relativedelta(years=1)).date(),
    end_date=get_utcnow().date())

survey = Survey(
    name='annual',
    position=0,
    map_area='test_community',
    start_date=(get_utcnow() - relativedelta(years=3)).date(),
    end_date=(get_utcnow() - relativedelta(years=2)).date(),
    full_enrollment_date=(get_utcnow() - relativedelta(years=2)).date()
)
bcpp_year_one.add_survey(survey)

survey = Survey(
    name='ahs',
    position=1,
    map_area='test_community',
    start_date=(get_utcnow() - relativedelta(years=2)).date(),
    end_date=(get_utcnow() - relativedelta(years=1)).date(),
    full_enrollment_date=(get_utcnow() - relativedelta(years=1)).date()
)
bcpp_year_two.add_survey(survey)

survey = Survey(
    name='ahs',
    position=1,
    map_area='test_community',
    start_date=(get_utcnow() - relativedelta(years=1)).date(),
    end_date=(get_utcnow()).date(),
    full_enrollment_date=(get_utcnow()).date()
)
bcpp_year_three.add_survey(survey)

site_surveys.register(bcpp_year_one)
site_surveys.register(bcpp_year_two)
site_surveys.register(bcpp_year_three)
