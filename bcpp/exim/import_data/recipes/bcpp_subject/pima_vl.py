# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

df_drop_columns = ['quota_pk', 'request_code']

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'poc_vl_type': lambda row: common_choices(row['poc_vl_type']),
    'vl_value_quatifier': lambda row: common_choices(row['vl_value_quatifier']),
    'easy_of_use': lambda row: common_choices(row['easy_of_use']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.pimavl',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
