from ...recipe import site_recipes, Recipe


site_recipes.register(Recipe(
    model_name='household.householdassessment'))

site_recipes.register(Recipe(
    model_name='household.householdrefusal'))

site_recipes.register(Recipe(
    model_name='household.householdrefusalhistory'))


df_drop_columns = [
    'survey_id',
]

site_recipes.register(Recipe(
    model_name='household.householdworklist',
    df_drop_columns=df_drop_columns))
