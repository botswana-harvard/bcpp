import arrow
import numpy as np
import pandas as pd
import re

from datetime import datetime
from dateutil.parser import parse

from django.db.models.fields import DateTimeField

from .exceptions import ImportDataError


class BaseImportCsv:

    """
    Usage:
        from bcpp.exim.import_data import site_recipes

        # test populate works with any errors
        for model_name, recipe in site_recipes.recipes.items():
            obj = ImportCsvToModel(recipe=recipe)
            obj.populate_model()

        # if no errors, save
        for model_name, recipe in site_recipes.recipes.items():
            obj = ImportCsvToModel(recipe=recipe)
            obj.populate_model(save=True)

    """

    def __init__(self, recipe=None, raise_errors=None):
        self._df = pd.DataFrame()
        self.read_csv_sep = recipe.read_csv_sep or '|'
        self.raise_errors = True if raise_errors is None else raise_errors
        self.column_names = None
        self.recipe = recipe
        self.row_handler = self.recipe.row_handler
        self.post_row_handler = self.recipe.post_row_handler
        self.post_import_handler = self.recipe.post_import_handler
        self.df_rename_columns = self.recipe.df_rename_columns
        self.df_drop_columns = self.recipe.df_drop_columns
        self.df_add_columns = self.recipe.df_add_columns
        self.df_copy_columns = self.recipe.df_copy_columns
        self.df_map_options = self.recipe.df_map_options
        self.df_apply_functions = self.recipe.df_apply_functions

    @property
    def df(self):
        """Returns a dataframe from the CSV at "recipe.in_path".
        """
        def date_parser(x):
            """Func to convert date/datetime string to timezone aware datetime.
            """
            if pd.isnull(x):
                return np.nan
            elif re.match('^[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{2}$', x):
                dt = parse(x, dayfirst=True)
            elif re.match('^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$', x):
                dt = datetime.strptime(x, '%Y-%m-%d')
            elif re.match('^[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}\:[0-9]{2}\:[0-9]{2}$', x):
                dt = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
            elif re.match('^[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}\:[0-9]{2}\:[0-9]{2}\+[0-9]{2}\:[0-9]{2}$', x):
                x = re.match(
                    '^[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}\:[0-9]{2}\:[0-9]{2}', x).group()
                dt = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
            elif re.match('^[0-9]{1,2}\/[0-9]{1,2}\/[0-9]{2} [0-9]{2}\:[0-9]{2}$', x):
                dt = parse(x, yearfirst=True)
            else:
                try:
                    dt = parse(x, yearfirst=True)
                except ValueError:
                    raise ImportDataError(
                        'Invalid date string. Got {}'.format(x))
            return arrow.Arrow.fromdatetime(dt).to('UTC').datetime

        if self._df.empty:
            df = pd.read_csv(
                self.recipe.in_path, low_memory=False, names=self.column_names,
                sep=self.read_csv_sep,
                encoding='utf-8',
                lineterminator='\n',
                escapechar='\\')
            parse_dates = self.date_columns(df)
            self._df = pd.read_csv(
                self.recipe.in_path, low_memory=False,
                parse_dates=parse_dates, date_parser=date_parser,
                sep=self.read_csv_sep,
                encoding='utf-8',
                lineterminator='\n',
                escapechar='\\')
            for column, copy_column in self.df_copy_columns.items():
                self._df[column] = self._df[copy_column]
            self._df = self._df.rename(columns=self.df_rename_columns)
            for column_name in self.df_add_columns:
                try:
                    self._df[column_name]
                except KeyError:
                    self._df[column_name] = np.NaN
            for column, options in self.df_map_options.items():
                self._df[column] = self._df[column].map(options.get)
            for column, func in self.df_apply_functions.items():
                self._df[column] = self._df.apply(
                    lambda row: func(row), axis=1)
            for column_name in self.df_drop_columns:
                self._df = self._df.drop(column_name, axis=1)
        return self._df

    def date_columns(self, df):
        """Returns a list of datetime column names in both the model
        and the dataframe.
        """
        datetime_columns = [f.name for f in self.datetime_fields]
        return [
            col for col in datetime_columns if col in list(df.columns)]

    @property
    def datetime_fields(self):
        """Returns a list of datetime fields.
        """
        datetime_fields = []
        for field in self.model._meta.get_fields():
            if isinstance(field, DateTimeField):
                datetime_fields.append(field)
        return datetime_fields

    @property
    def notnull_fields(self):
        """Returns a list of django field classes that do not accept null.
        """
        return [field for field in self.model._meta.get_fields(include_parents=False)
                if field.null is False]

    @property
    def choice_fields(self):
        """Returns a list of django field classes that do not accept null.
        """
        if not self._choice_fields:
            for field in self.model._meta.get_fields(include_parents=False):
                try:
                    if field.choices:
                        self._choice_fields.update({field.name: field.choices})
                except AttributeError:
                    pass
        return self._choice_fields

    def convert_nan(self, pd_row):
        """Return a row with np.nan converted to python None.

        If text field does not accept null insert an empty string.
        """
        for k in pd_row:
            if pd.isnull(pd_row[k]):
                if (k in [f.name for f in self.notnull_fields
                          if f.get_internal_type() in ['CharField', 'TextField']]):
                    pd_row.update({k: ''})
                else:
                    pd_row.update({k: None})
        return pd_row
