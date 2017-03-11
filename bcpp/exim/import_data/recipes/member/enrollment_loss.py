from ...model_recipe import ModelRecipe
from ...recipe import site_recipes


site_recipes.register(ModelRecipe(
    model_name='member.enrollmentloss',
    old_model_name='bcpp_household_member.enrollmentloss',
))
