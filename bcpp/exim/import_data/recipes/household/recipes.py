from ...model_recipe import ModelRecipe
from ...recipe import site_recipes


site_recipes.register(ModelRecipe(
    model_name='household.householdassessment',
    old_model_name='bcpp_household.householdassessment',
))

site_recipes.register(ModelRecipe(
    model_name='household.householdrefusal',
    old_model_name='bcpp_household.householdrefusal',
))

site_recipes.register(ModelRecipe(
    model_name='household.householdrefusalhistory',
    old_model_name='bcpp_household.householdrefusalhistory',
))


df_drop_columns = [
    'survey_id',
]

site_recipes.register(ModelRecipe(
    model_name='household.householdworklist',
    old_model_name='bcpp_household.householdworklist',
    df_drop_columns=df_drop_columns))
