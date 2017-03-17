from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .common_choices import common_choices


df_drop_columns = []

df_add_columns = []

df_rename_columns = []

df_apply_functions = {
    'why_not_tested': lambda row: common_choices(row['why_not_tested']),
}

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.hivresult',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))
