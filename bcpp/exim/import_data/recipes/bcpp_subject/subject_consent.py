from edc_constants.constants import NO

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from ..household.household_structure import survey_schedule


df_drop_columns = [
    'registered_subject_id',
    'study_site_id',
    'community']

df_rename_columns = {
    'survey_id': 'survey_schedule'}

df_apply_functions = {
    'is_minor': lambda row: NO if row['is_minor'] == '-' else row['is_minor'],
    'is_incarcerated': lambda row: NO if row['is_incarcerated'] == '-' else row['is_incarcerated'],
    'survey_schedule': lambda row: survey_schedule(row),
    'is_signed': lambda row: 1 if row['is_signed'] is True else 0,
    'is_verified': lambda row: 1 if row['is_verified'] is True else 0,
}


site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.subjectconsent',
    df_drop_columns=df_drop_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))
