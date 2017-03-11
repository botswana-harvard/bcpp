from edc_constants.constants import NOT_APPLICABLE, NO

from member.choices import CONTINUE_PARTICIPATION

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes

df_apply_functions = {
    'guardian': lambda row: NOT_APPLICABLE if row['guardian'] == '-' else row['guardian'],
    'confirm_participation': (
        lambda row: CONTINUE_PARTICIPATION
        if row['confirm_participation'] == NO else row['confirm_participation']),
}


site_recipes.register(ModelRecipe(
    model_name='member.enrollmentchecklist',
    old_model_name='bcpp_household_member.enrollmentchecklist',
    df_apply_functions=df_apply_functions,
))
