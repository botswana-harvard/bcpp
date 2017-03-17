from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices
from edc_constants.constants import OTHER, DWTA, NOT_SURE


def verbal_hiv_result(value):
    if value == 'Other':
        return OTHER
    elif value == 'not_answering':
        return DWTA
    elif value == 'Don\'t want to answer':
        return DWTA
    elif value == 'Not Sure':
        return NOT_SURE
    return value


df_drop_columns = []

df_add_columns = []

df_rename_columns = []

df_apply_functions = {
    'has_record': lambda row: common_choices(row['has_record']),
    'verbal_hiv_result': lambda row: verbal_hiv_result(row['verbal_hiv_result']),
    'when_hiv_test': lambda row: common_choices(row['when_hiv_test']),
}

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.hivtestinghistory',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))
