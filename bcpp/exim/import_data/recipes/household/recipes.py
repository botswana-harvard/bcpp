from ...model_recipe import ModelRecipe
from ...recipe import site_recipes


site_recipes.register(ModelRecipe(
    model_name='household.householdassessment'))

site_recipes.register(ModelRecipe(
    model_name='household.householdrefusal'))

site_recipes.register(ModelRecipe(
    model_name='household.householdrefusalhistory'))


df_drop_columns = [
    'survey_id',
]

site_recipes.register(ModelRecipe(
    model_name='household.householdworklist',
    df_drop_columns=df_drop_columns))
