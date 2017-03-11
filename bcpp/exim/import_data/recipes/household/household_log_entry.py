from household.constants import ELIGIBLE_REPRESENTATIVE_PRESENT

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes


def household_status(row):
    if row['household_status'] == 'occupied':
        return ELIGIBLE_REPRESENTATIVE_PRESENT
    else:
        return row['household_status']

df_apply_functions = {'household_status': lambda row: household_status(row)}


site_recipes.register(ModelRecipe(
    model_name='household.householdlogentry',
    old_model_name='bcpp_household.householdlogentry',
    df_apply_functions=df_apply_functions))
