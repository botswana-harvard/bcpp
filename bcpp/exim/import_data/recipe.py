import pandas as pd
import os

from collections import OrderedDict


class AlreadyRegistered(Exception):
    pass


class Recipe:

    name = None
    import_csv_class = None

    def __init__(self, row_handler=None, post_row_handler=None,
                 post_import_handler=None,
                 df_map_options=None, df_apply_functions=None,
                 df_rename_columns=None, df_drop_columns=None):
        self._df = pd.DataFrame()
        self.in_path = None  # set in child class
        self.out_path = None  # set in child class
        # manipulate dataframe columns
        self.df_rename_columns = df_rename_columns or {}
        self.df_drop_columns = df_drop_columns or []
        self.df_map_options = df_map_options or {}
        self.df_apply_functions = df_apply_functions or {}
        # manipulate single row as dictionary (read from df)
        self.row_handler = row_handler
        self.post_row_handler = post_row_handler
        self.post_import_handler = post_import_handler

    def import_csv(self, **kwargs):
        self.import_csv_class(recipe=self, **kwargs)

    @property
    def df(self):
        if self._df.empty:
            obj = self.import_csv_class(recipe=self)
            self._df = obj.df
        return self._df


class Recipes:

    def __init__(self):
        self._registry = OrderedDict()

    def register(self, recipe):
        if recipe.name in self._registry:
            raise AlreadyRegistered(
                'Recipe {} is already registered.'.format(recipe.name))
        self._registry.update({recipe.name: recipe})

    @property
    def recipes(self):
        return self._registry

    def run_model_recipe(self, save=None, app_label=None, label_lower=None, debug=None):
        for recipe in self.recipes.values():
            if label_lower and label_lower != recipe.model._meta.label_lower:
                continue
            elif app_label and app_label != recipe.model._meta.app_label:
                continue
            recipe.import_csv(recipe=recipe, save=save, debug=debug)

    def run(self, save=None, debug=None):
        for recipe in self.recipes.values():
            recipe.import_csv(recipe=recipe, save=save, debug=debug)

site_recipes = Recipes()
