# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = {
    'enacted_phyical_stigma': 'enacted_physical_stigma'}

df_apply_functions = {
    'test_community_stigma': lambda row: common_choices(row['test_community_stigma']),
    'gossip_community_stigma': lambda row: common_choices(row['gossip_community_stigma']),
    'respect_community_stigma': lambda row: common_choices(row['respect_community_stigma']),
    'enacted_verbal_stigma': lambda row: common_choices(row['enacted_verbal_stigma']),
    'enacted_physical_stigma': lambda row: common_choices(row['enacted_physical_stigma']),
    'enacted_family_stigma': lambda row: common_choices(row['enacted_family_stigma']),
    'fear_stigma': lambda row: common_choices(row['fear_stigma']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.stigmaopinion',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
