import sys

import pandas as pd

from shutil import copyfile
from collections import OrderedDict

from ..export_data.export_data import ExportDataToCsv
import csv


class AlreadyRegistered(Exception):
    pass


class Recipe:

    name = None
    import_csv_class = None
    export_csv_class = ExportDataToCsv

    def __init__(self, row_handler=None, post_row_handler=None,
                 post_import_handler=None,
                 df_map_options=None, df_apply_functions=None,
                 df_rename_columns=None, df_drop_columns=None,
                 df_add_columns=None, df_copy_columns=None,
                 read_csv_sep=None, **kwargs):
        self._df = pd.DataFrame()
        self._raw_df = pd.DataFrame()
        self.read_csv_sep = read_csv_sep or '|'
        self.in_path = None  # set in child class
        self.out_path = None  # set in child class
        # manipulate dataframe columns
        self.df_rename_columns = df_rename_columns or {}
        self.df_drop_columns = df_drop_columns or []
        self.df_add_columns = df_add_columns or []
        self.df_copy_columns = df_copy_columns or {}
        self.df_map_options = df_map_options or {}
        self.df_apply_functions = df_apply_functions or {}
        # manipulate single row as dictionary (read from df)
        self.row_handler = row_handler
        self.post_row_handler = post_row_handler
        self.post_import_handler = post_import_handler

    def import_csv(self, fix_sep=None, **kwargs):
        if fix_sep:
            copyfile(self.in_path, self.in_path + '.old')
            df = pd.read_csv(
                self.in_path,
                low_memory=False,
                encoding='utf-8',
                sep=',')
            df.to_csv(
                path_or_buf=self.in_path,
                index=False,
                encoding='utf-8',
                sep='|',
                quoting=csv.QUOTE_MINIMAL,
                quotechar='"',
                line_terminator='\n',
                escapechar='\\')
        self.import_csv_class(recipe=self, **kwargs)

    def export_df(self, path_or_buf=None, sep=None, columns=None, **kwargs):
        """Export the final dataframe to CSV.

        Default options are optimized for mysql OUTFILE.
        """
        options = dict(
            path_or_buf=path_or_buf or self.out_path,
            index=False,
            encoding='utf-8',
            sep=sep or '|',
            quoting=csv.QUOTE_MINIMAL,
            quotechar='"',
            line_terminator='\n',
            na_rep='NULL',
            escapechar='\\')
        if columns:
            options.update(columns=columns)
        self.df.to_csv(**options)

    def export_raw_df(self, read_csv_sep=None):
        """Export the "raw" dataframe to CSV using the PIPE delimiter.
        """
        if read_csv_sep:
            sep = self.read_csv_sep
            self.read_csv_sep = read_csv_sep
        self.raw_df.to_csv(
            path_or_buf=self.in_path,
            index=False,
            encoding='utf-8',
            sep='|',
            quoting=3,
            line_terminator='\n',
            escapechar='\\')
        sys.stdout.write('Exported outfile to {}'.format(self.in_path))
        if read_csv_sep:
            self.read_csv_sep = sep

    @property
    def raw_df(self):
        """Dataframe before any processing (rename, drop, apply).
        """
        if self._raw_df.empty:
            self._raw_df = pd.read_csv(
                self.in_path, low_memory=False,
                encoding='utf-8',
                sep='|',
                lineterminator='\n',
                escapechar='\\')
        return self._raw_df

    @property
    def df(self):
        """Dataframe after processing (rename, drop, apply).
        """
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
