# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'mobility': lambda row: common_choices(row['mobility']),
    'self_care': lambda row: common_choices(row['self_care']),
    'activities': lambda row: common_choices(row['activities']),
    'pain': lambda row: common_choices(row['pain']),
    'anxiety': lambda row: common_choices(row['anxiety']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.qualityoflife',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
