from edc_constants.constants import DWTA

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes
from .household_info import *
from .household_member import *
from .representative_eligibility import *


site_recipes.register(ModelRecipe(
    model_name='member.householdheadeligibility',
))

site_recipes.register(ModelRecipe(
    model_name='member.enrollmentchecklist',
))

site_recipes.register(ModelRecipe(
    model_name='member.enrollmentloss',
))

site_recipes.register(ModelRecipe(
    model_name='member.absentmember',
))

site_recipes.register(ModelRecipe(
    model_name='member.undecidedmember',
))

site_recipes.register(ModelRecipe(
    model_name='member.undecidedmemberhistory',
))

site_recipes.register(ModelRecipe(
    model_name='member.refusedmember',
))

site_recipes.register(ModelRecipe(
    model_name='member.refusedmemberhistory',
))

site_recipes.register(ModelRecipe(
    model_name='member.deceasedmember',
))

site_recipes.register(ModelRecipe(
    model_name='member.htcmember',
))

site_recipes.register(ModelRecipe(
    model_name='member.htcmemberhistory',
))
