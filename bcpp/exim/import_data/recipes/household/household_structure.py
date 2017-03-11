import pandas as pd

from household.models import HouseholdStructure

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes


def survey_schedule(row):
    if row['survey_schedule'] == 'd88badb3-e7c8-11e3-89a3-a82066234239':
        return 'bcpp-survey.bcpp-year-1.test_community'
    elif row['survey_schedule'] == 'd88f61a1-e7c8-11e3-b1af-a82066234239':
        return 'bcpp-survey.bcpp-year-2.test_community'
    elif row['survey_schedule'] == 'd88d5fc2-e7c8-11e3-9907-a82066234239':
        return 'bcpp-survey.bcpp-year-3.test_community'

df_rename_columns = {
    'survey_id': 'survey_schedule'}

df_apply_functions = {
    'survey_schedule': lambda row: survey_schedule(row),
    'report_datetime': lambda row: row['created'],
    'user_created': lambda row: 'erikvw' if pd.isnull(row['user_created']) else row['user_created'],
    'enrolled': lambda row: False if pd.isnull(row['enrolled']) else True,
}


def post_import_handler():
    for obj in HouseholdStructure.objects.all():
        obj.survey_schedule = obj.survey_schedule.replace(
            'test_community', obj.household.plot.map_area)
        obj.save_base(raw=True)

site_recipes.register(ModelRecipe(
    model_name='household.householdstructure',
    old_model_name='bcpp_household.householdstructure',
    df_apply_functions=df_apply_functions,
    df_rename_columns=df_rename_columns))
