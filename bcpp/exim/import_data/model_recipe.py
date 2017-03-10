import os

from django.apps import apps as django_apps

from .import_csv_to_model import ImportCsvToModel
from .recipe import Recipe
from .settings import UPDATED_DIR


class ModelRecipe(Recipe):

    import_csv_class = ImportCsvToModel

    def __init__(self, model_name=None, m2m_recipes=None, **kwargs):
        super().__init__(**kwargs)
        self.name = model_name
        self.model = django_apps.get_model(*model_name.split('.'))
        csv_filename = self.csv_filename or '{}.csv'.format(
            model_name.split('.')[1])
        self.path = os.path.join(
            UPDATED_DIR, self.model._meta.app_label, csv_filename)
        self.m2m_recipes = m2m_recipes

    def import_csv(self, save=None, debug=None):
        super().import_csv(save=save, debug=debug)
        for m2m_recipe in self.m2m_recipes:
            m2m_recipe.run()
