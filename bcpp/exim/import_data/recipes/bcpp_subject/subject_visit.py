import uuid

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from ..household.household_structure import survey_schedule

df_drop_columns = ['info_source_other']

df_add_columns = ['survey_schedule']

df_rename_columns = []

df_apply_functions = {
    'survey_schedule': lambda row: survey_schedule(row),
    'appointment_id': lambda row: uuid.UUID(row['appointment_id']),
}

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.subjectvisit',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))
