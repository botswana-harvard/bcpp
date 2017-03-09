from ...recipe import site_recipes, Recipe


df_drop_columns = [
    'may_store_samples',
    'survival_status',
    'hiv_status',
    'study_site_id',
    'salt',
]

site_recipes.register(Recipe(
    model_name='edc_registration.registeredsubject',
    df_drop_columns=df_drop_columns))
