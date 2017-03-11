import os

from django.apps import apps as django_apps

from .import_csv_to_model import ImportCsvToModel
from .recipe import Recipe
from .settings import UPDATED_DIR
from bcpp.exim.import_data.settings import SOURCE_DIR


class ModelRecipe(Recipe):

    import_csv_class = ImportCsvToModel

    def __init__(self, model_name=None, old_model_name=None, m2m_recipes=None, **kwargs):
        super().__init__(**kwargs)
        self.name = model_name
        self.model = django_apps.get_model(*model_name.split('.'))
        old_model_name = old_model_name or model_name
        self.in_path = os.path.join(
            SOURCE_DIR,
            old_model_name.split('.')[0],
            '{}.csv'.format(old_model_name.split('.')[1]))
        self.out_path = os.path.join(
            UPDATED_DIR,
            self.model._meta.app_label,
            '{}.csv'.format(model_name.split('.')[1]))
        self.m2m_recipes = m2m_recipes or []

    def import_csv(self, save=None, **kwargs):
        super().import_csv(save=save, **kwargs)
        if save:
            for m2m_recipe in self.m2m_recipes:
                m2m_recipe.run()
