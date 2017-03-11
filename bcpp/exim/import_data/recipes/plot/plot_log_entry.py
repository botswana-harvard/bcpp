import pandas as pd
import numpy as np

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes

df_apply_functions = {
    'report_date': lambda row: row['report_datetime'],
    'log_status': lambda row: np.NaN if pd.isnull(row['log_status']) else row['log_status'].lower()
}

site_recipes.register(ModelRecipe(
    model_name='plot.plotlogentry',
    old_model_name='bcpp_household.plotlogentry',
    df_apply_functions=df_apply_functions))
