# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices
from edc_constants.constants import YES, NO


def permanent_resident(value):
    value = common_choices(value)
    if value == 'True':
        return YES
    elif value == 'False':
        return NO
    return value

df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'nights_away': lambda row: common_choices(row['nights_away']),
    'length_residence': lambda row: common_choices(row['length_residence']),
    'permanent_resident': lambda row: permanent_resident(row['permanent_resident']),
    'intend_residency': lambda row: common_choices(row['intend_residency']),
    'cattle_postlands': lambda row: common_choices(row['cattle_postlands']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.residencymobility',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
