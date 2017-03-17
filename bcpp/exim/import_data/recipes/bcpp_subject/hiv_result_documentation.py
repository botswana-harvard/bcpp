from edc_constants.constants import UNKNOWN

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes


df_drop_columns = []

df_add_columns = []

df_rename_columns = []

df_apply_functions = {
    'result_recorded': lambda row: UNKNOWN if row['result_recorded'] == 'UNK' else row['result_recorded'],
}

site_recipes.register(ModelRecipe(
    model_name='bcpp_subject.hivresultdocumentation',
    df_drop_columns=df_drop_columns,
    df_add_columns=df_add_columns,
    df_rename_columns=df_rename_columns,
    df_apply_functions=df_apply_functions,
))
