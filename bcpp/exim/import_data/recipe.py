import os

from collections import OrderedDict

from .settings import UPDATED_DIR


class AlreadyRegistered(Exception):
    pass


class Recipe:

    name = None
    import_csv_class = None

    def __init__(self, csv_filename=None,
                 row_handler=None, post_row_handler=None, post_import_handler=None,
                 df_map_options=None, df_apply_functions=None,
                 df_rename_columns=None, df_drop_columns=None):
        self.csv_filename = csv_filename
        self.path = os.path.join(UPDATED_DIR or '', csv_filename or '')
        # manipulate dataframe columns
        self.df_rename_columns = df_rename_columns or {}
        self.df_drop_columns = df_drop_columns or []
        self.df_map_options = df_map_options or {}
        self.df_apply_functions = df_apply_functions or {}
        # manipulate single row as dictionary (read from df)
        self.row_handler = row_handler
        self.post_row_handler = post_row_handler
        self.post_import_handler = post_import_handler

    def import_csv(self, save=None, debug=None):
        self.import_csv_class(recipe=self, save=save, debug=debug)

    def df(self):
        obj = self.import_csv_class(recipe=self)
        return obj.df


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
