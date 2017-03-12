from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from bcpp.exim.import_data.recipes.household.household_structure import survey_schedule


def schedule_name(row):
    if row['visit_definition_id'] == '3138f9da-0e57-4d0a-8afd-761f096203d6':
        return 'cln_schedule'
    elif row['visit_definition_id'] == 'dab10682-e7c8-11e3-8dc4-a82066234239':
        return 'bhs_schedule'
    elif row['visit_definition_id'] == '6082137a-9a30-4e59-9755-36c4f22f29cc':
        return 'ahs_schedule'
    elif row['visit_definition_id'] == 'a55f212a-d357-4fe2-a334-dd9fcf8d17e0':
        return 'ahs_schedule'


def visit_code(row):
    if row['visit_definition_id'] == '3138f9da-0e57-4d0a-8afd-761f096203d6':
        return 'C0'
    elif row['visit_definition_id'] == 'dab10682-e7c8-11e3-8dc4-a82066234239':
        return 'T0'
    elif row['visit_definition_id'] == '6082137a-9a30-4e59-9755-36c4f22f29cc':
        return 'T1'
    elif row['visit_definition_id'] == 'a55f212a-d357-4fe2-a334-dd9fcf8d17e0':
        return 'T2'

df_drop_columns = []

df_rename_columns = []

df_add_columns = [
    'survey_schedule', 'visit_schedule_name', 'schedule_name', 'visit_code']

df_apply_functions = {
    'visit_code': lambda row: visit_code(row),
    'schedule_name': lambda row: schedule_name(row),
    'visit_schedule_name': lambda row: visit_schedule_name(row),
    'survey_schedule': lambda row: survey_schedule(row),
}

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.appointment',
    old_model_name='appointment.appointment',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))
