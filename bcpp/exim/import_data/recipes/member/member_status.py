from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from ..household.household_structure import survey_schedule
from edc_constants.constants import DWTA


def refusal_reason(row):
    if row['reason'] == 'not_answering':
        return DWTA
    return row['reason']

df_drop_columns = [
    'registered_subject_id']

df_rename_columns = {
    'survey_id': 'survey_schedule'}

df_apply_functions = {
    'survey_schedule': lambda row: survey_schedule(row)}

site_recipes.register(ModelRecipe(
    model_name='member.absentmember',
    old_model_name='bcpp_household_member.subjectabsentee',
    df_drop_columns=df_drop_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))

site_recipes.register(ModelRecipe(
    model_name='member.undecidedmember',
    old_model_name='bcpp_household_member.subjectundecided',
    df_drop_columns=df_drop_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))

site_recipes.register(ModelRecipe(
    model_name='member.undecidedmemberhistory',
    old_model_name='bcpp_household_member.subjectundecidedhistory',
    df_drop_columns=df_drop_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))

site_recipes.register(ModelRecipe(
    model_name='member.refusedmember',
    old_model_name='bcpp_household_member.subjectrefusal',
    df_drop_columns=df_drop_columns,
    df_rename_columns=dict(
        {'subject_refusal_status': 'refused_member_status'}, **df_rename_columns),
    df_apply_functions=dict(
        {'reason': lambda row: refusal_reason(row)},
        **df_apply_functions),
))

site_recipes.register(ModelRecipe(
    model_name='member.refusedmemberhistory',
    old_model_name='bcpp_household_member.subjectrefusalhistory',
    df_drop_columns=df_drop_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))

site_recipes.register(ModelRecipe(
    model_name='member.deceasedmember',
    old_model_name='bcpp_household_member.subjectdeath',
    df_drop_columns=df_drop_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))

site_recipes.register(ModelRecipe(
    model_name='member.htcmember',
    old_model_name='bcpp_household_member.subjecthtc',
    df_drop_columns=df_drop_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))

site_recipes.register(ModelRecipe(
    model_name='member.htcmemberhistory',
    old_model_name='bcpp_household_member.subjecthtcmember',
    df_drop_columns=df_drop_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))
