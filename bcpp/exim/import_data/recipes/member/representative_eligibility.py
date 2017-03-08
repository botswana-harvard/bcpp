from member.models import RepresentativeEligibility

from ...recipe import site_recipes, Recipe


def post_import_handler():
    for obj in RepresentativeEligibility.objects.all():
        obj.survey_schedule = obj.household_structure.survey_schedule
        obj.save_base(raw=True)


site_recipes.register(Recipe(
    model_name='member.representativeeligibility',
    post_import_handler=post_import_handler))
