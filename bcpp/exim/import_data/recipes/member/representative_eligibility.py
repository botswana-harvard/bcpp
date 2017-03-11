from member.models import RepresentativeEligibility

from ...model_recipe import ModelRecipe
from ...recipe import site_recipes


def post_import_handler():
    for obj in RepresentativeEligibility.objects.all():
        obj.survey_schedule = obj.household_structure.survey_schedule
        obj.save_base(raw=True)


site_recipes.register(ModelRecipe(
    model_name='member.representativeeligibility',
    old_model_name='bcpp_household.representativeeligibility',
    post_import_handler=post_import_handler))
