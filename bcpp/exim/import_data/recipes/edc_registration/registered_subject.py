from ...model_recipe import ModelRecipe
from ...recipe import site_recipes


df_drop_columns = [
    'may_store_samples',
    'survival_status',
    'hiv_status',
    'study_site_id',
    'salt',
]

site_recipes.register(ModelRecipe(
    model_name='edc_registration.registeredsubject',
    old_model_name='edc_registration.registeredsubject',
    df_drop_columns=df_drop_columns))
