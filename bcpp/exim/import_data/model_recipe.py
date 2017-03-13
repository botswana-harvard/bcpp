import os
import uuid

import pandas as pd

from django.apps import apps as django_apps

from .import_csv_to_model import ImportCsvToModel
from .recipe import Recipe
from .settings import UPDATED_DIR, SOURCE_DIR
from edc_pdutils.model_to_dataframe import ModelToDataFrame


class ModelRecipe(Recipe):

    import_csv_class = ImportCsvToModel

    def __init__(self, model_name=None, old_model_name=None, m2m_recipes=None, **kwargs):
        super().__init__(**kwargs)
        self._model_df = pd.DataFrame()
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
        self.df_apply_functions.update({
            'id': lambda row: uuid.UUID(row['id']),
            'user_modified': lambda row: (
                row['user_created']
                if (pd.isnull(row['user_modified']) or ''.join(row['user_modified'].split()) == '')
                else row['user_modified'])})

    def import_csv(self, save=None, **kwargs):
        super().import_csv(save=save, **kwargs)
        if save:
            for m2m_recipe in self.m2m_recipes:
                m2m_recipe.run()

    @property
    def model_df(self):
        """Returns a DataFrame built from the model.
        """
        if self._model_df.empty:
            obj = ModelToDataFrame(self.model)
            self._model_df = obj.dataframe
        return self._model_df
