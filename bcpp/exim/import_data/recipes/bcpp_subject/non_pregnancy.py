# from ...m2m_recipe import M2mRecipe
from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = {}

df_apply_functions = {
    'more_children': lambda row: common_choices(row['more_children']),
    'anc_last_pregnancy': lambda row: common_choices(row['anc_last_pregnancy']),
    'hiv_last_pregnancy': lambda row: common_choices(row['hiv_last_pregnancy']),
    'preg_arv': lambda row: common_choices(row['preg_arv']),
}

m2m_recipes = []

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.nonpregnancy',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
    m2m_recipes=m2m_recipes,
))
