import pandas as pd

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes

df_drop_columns = [
    'gps_lon',
    'gps_lat',
    'gps_target_lon',
    'gps_target_lat',
    'community',
    'target_radius',
    'gps_degrees_s',
    'gps_degrees_e',
    'gps_minutes_e',
    'gps_minutes_s',
    'replaceable',
    'hh_seed',
    'replaced_by',
    'uploaded_map',
    'hh_int',
    'action',
]

df_apply_functions = {
    'household_sequence': lambda row: int(row['household_identifier'][-2:]),
    'report_datetime': lambda row: row['created'],
    'user_created': lambda row: 'erikvw' if pd.isnull(row['user_created']) else row['user_created'],
}


site_recipes.register(ModelRecipe(
    model_name='household.household',
    old_model_name='bcpp_household.household',
    df_drop_columns=df_drop_columns,
    df_apply_functions=df_apply_functions))
