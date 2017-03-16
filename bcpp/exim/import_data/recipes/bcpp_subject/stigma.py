# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'anticipate_stigma': lambda row: common_choices(row['anticipate_stigma']),
    'enacted_shame_stigma': lambda row: common_choices(row['enacted_shame_stigma']),
    'saliva_stigma': lambda row: common_choices(row['saliva_stigma']),
    'teacher_stigma': lambda row: common_choices(row['teacher_stigma']),
    'children_stigma': lambda row: common_choices(row['children_stigma']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.stigma',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
