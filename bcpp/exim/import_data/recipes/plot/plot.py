import pandas as pd
import numpy as np

from edc_constants.constants import WEEKENDS, WEEKDAYS

from plot.constants import NON_RESIDENTIAL, TWENTY_PERCENT, FIVE_PERCENT

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes


"""UPDATE plot_plot as A
LEFT JOIN bhp066.bcpp_household_plot as B ON A.id=B.id
SET A.selected=B.selected;
"""


def fix_status(row):
    if row['status'] == 'bcpp_clinic':
        return np.NaN
    elif row['status'] == 'non-residential':
        return NON_RESIDENTIAL
    else:
        return row['status']

df_rename_columns = {
    'gps_lon': 'gps_confirmed_longitude',
    'gps_lat': 'gps_confirmed_latitude',
    'community': 'map_area',
    'device_id': 'device_created',
}

df_drop_columns = [
    'uploaded_map_16',
    'uploaded_map_17',
    'uploaded_map_18',
    'gps_degrees_e',
    'gps_degrees_s',
    'gps_minutes_e',
    'gps_minutes_s',
    'replaceable',
    'replaces',
    'replaced_by',
    'bhs',
    'action']


df_map_options = {
    'time_of_week': {
        'weekend': WEEKENDS,
        'weekday': WEEKDAYS},
    'selected': {
        '1.0': '1',
        '2.0': '2'},
}

df_apply_functions = {
    'confirmed': (
        lambda row: True if (row['gps_confirmed_longitude'] and row[
            'gps_confirmed_latitude']) else False),
    'device_created': (
        lambda row: '99' if pd.isnull(row['device_created']) else row['device_created']),
    'device_modified': lambda row: row['device_created'],
    'status': lambda row: fix_status(row),
    'rss': lambda row: True if row['selected'] in [TWENTY_PERCENT, FIVE_PERCENT] else False
}


site_recipes.register(ModelRecipe(
    model_name='plot.plot',
    old_model_name='bcpp_household.plot',
    df_rename_columns=df_rename_columns,
    df_drop_columns=df_drop_columns,
    df_map_options=df_map_options,
    df_apply_functions=df_apply_functions))
