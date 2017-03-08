from household.constants import ELIGIBLE_REPRESENTATIVE_PRESENT

from ...recipe import site_recipes, Recipe


def household_status(row):
    if row['household_status'] == 'occupied':
        return ELIGIBLE_REPRESENTATIVE_PRESENT
    else:
        return row['household_status']

df_apply_functions = {'household_status': lambda row: household_status(row)}


site_recipes.register(Recipe(
    model_name='household.householdlogentry',
    df_apply_functions=df_apply_functions))
