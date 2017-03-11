from ...model_recipe import ModelRecipe
from ...recipe import site_recipes

site_recipes.register(ModelRecipe(
    model_name='member.householdheadeligibility',
    old_model_name='bcpp_household_member.householdheadeligibility',
))
