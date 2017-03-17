from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices

df_drop_columns = []

df_add_columns = []

df_rename_columns = []

df_apply_functions = {
    'where_hiv_test': lambda row: common_choices(row['where_hiv_test']),
    'why_hiv_test': lambda row: common_choices(row['why_hiv_test']),
    'arvs_hiv_test': lambda row: common_choices(row['arvs_hiv_test']),
    'hiv_pills': lambda row: common_choices(row['hiv_pills']),
}

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.hivtested',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))
