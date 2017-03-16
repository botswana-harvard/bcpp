# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices as base_common_choices
from edc_constants.constants import NOT_APPLICABLE


def common_choices(value):
    value = base_common_choices(value)
    if value == 'THE CLIENT WAS ALREADY ON ART':
        return NOT_APPLICABLE

df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'pima_today_other': lambda row: common_choices(row['pima_today_other'])}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.pimacd4',
    old_model_name='bcpp_subject.pima',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
