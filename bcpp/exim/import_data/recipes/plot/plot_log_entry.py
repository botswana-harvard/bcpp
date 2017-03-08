import pandas as pd
import numpy as np

from ...recipe import site_recipes, Recipe

# from plot.constants import ACCESSIBLE, INACCESSIBLE

df_apply_functions = {
    'report_date': lambda row: row['report_datetime'],
    'log_status': lambda row: np.NaN if pd.isnull(row['log_status']) else row['log_status'].lower()
}

site_recipes.register(Recipe(
    model_name='plot.plotlogentry',
    df_apply_functions=df_apply_functions))
