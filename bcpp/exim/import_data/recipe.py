from collections import OrderedDict

from django.apps import apps as django_apps

from .import_data import ImportDataFromCsv


class AlreadyRegistered(Exception):
    pass


class Recipe:

    def __init__(self, model_name=None, csv_filename=None, row_handler=None,
                 post_row_handler=None, post_import_handler=None,
                 df_map_options=None, df_apply_functions=None,
                 df_rename_columns=None, df_drop_columns=None):
        self.model_name = model_name
        self.csv_filename = csv_filename or '{}.csv'.format(
            model_name.split('.')[1])
        # manipulate dataframe columns
        self.df_rename_columns = df_rename_columns or {}
        self.df_drop_columns = df_drop_columns or []
        self.df_map_options = df_map_options or {}
        self.df_apply_functions = df_apply_functions or {}
        # manipulate single row as dictionary (read from df)
        self.row_handler = row_handler
        self.post_row_handler = post_row_handler
        self.post_import_handler = post_import_handler
        self.model = django_apps.get_model(*model_name.split('.'))


class Recipes:

    def __init__(self):
        self._registry = OrderedDict()

    def register(self, recipe):
        if recipe.model_name in self._registry:
            raise AlreadyRegistered(
                'Recipe {} is already registered.'.format(recipe.model_name))
        self._registry.update({recipe.model_name: recipe})

    @property
    def recipes(self):
        return self._registry

    def run(self, save=None, app_label=None, label_lower=None, debug=None):
        for recipe in self.recipes.values():
            if label_lower and label_lower != recipe.model._meta.label_lower:
                continue
            elif app_label and app_label != recipe.model._meta.app_label:
                continue
            obj = ImportDataFromCsv(recipe=recipe)
            obj.populate_model(save=save, debug=debug)

site_recipes = Recipes()
