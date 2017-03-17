from ...model_recipe import ModelRecipe
from ...recipe import site_recipes


df_drop_columns = []

df_add_columns = []

df_rename_columns = []

df_apply_functions = {}

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.elisahivresult',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))
