# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'internalize_stigma': lambda row: common_choices(row['internalize_stigma']),
    'internalized_stigma': lambda row: common_choices(row['internalized_stigma']),
    'friend_stigma': lambda row: common_choices(row['friend_stigma']),
    'family_stigma': lambda row: common_choices(row['family_stigma']),
    'enacted_talk_stigma': lambda row: common_choices(row['enacted_talk_stigma']),
    'enacted_respect_stigma': lambda row: common_choices(row['enacted_respect_stigma']),
    'enacted_jobs_tigma': lambda row: common_choices(row['enacted_jobs_tigma']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.positiveparticipant',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
