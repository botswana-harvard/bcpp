import re
import arrow
import numpy as np
import os
import pandas as pd
import sys

from collections import OrderedDict
from datetime import datetime
from pprint import pprint

from django.db.models.fields import DateTimeField
from django.db.utils import IntegrityError


class ImportDataError(Exception):
    pass


class ImportDataFromCsv:

    """
    Usage:
        from bcpp.exim.import_data import site_recipes

        # test populate works with any errors
        for model_name, recipe in site_recipes.recipes.items():
            obj = ImportDataFromCsv(recipe=recipe)
            obj.populate_model()

        # if no errors, save
        for model_name, recipe in site_recipes.recipes.items():
            obj = ImportDataFromCsv(recipe=recipe)
            obj.populate_model(save=True)

    """

    def __init__(self, recipe=None, path=None):
        self._df = pd.DataFrame()
        self._choice_fields = {}
        self.path = path or os.path.join(
            '/Users/erikvw/bcpp_201703/new/',
            recipe.model._meta.app_label, recipe.csv_filename)
        self.model = recipe.model
        self.row_handler = recipe.row_handler
        self.post_row_handler = recipe.post_row_handler
        self.post_import_handler = recipe.post_import_handler
        self.df_rename_columns = recipe.df_rename_columns
        self.df_drop_columns = recipe.df_drop_columns
        self.df_map_options = recipe.df_map_options
        self.df_apply_functions = recipe.df_apply_functions

    def populate_model(self, save=None, debug=None):
        start = datetime.now()
        sys.stdout.write('{} ...\r'.format(self.model._meta.label_lower))
        row_count = len(self.df)
        rows = (OrderedDict(row) for i, row in self.df.iterrows())
        for index, row in enumerate(rows):
            sys.stdout.write(
                '{} ...{}/{}  \r'.format(self.model._meta.label_lower, index, row_count))
            if debug:
                pprint(row)
            row = self.convert_nan(row)
            if self.row_handler:
                row = self.row_handler(row)
            self.validate_choice_fields(row)
            obj = self.model(**row)
            if save:
                try:
                    obj.save_base(raw=True)
                except IntegrityError as e:
                    raise IntegrityError('{}. Got {}'.format(str(e), obj.id))
                if self.post_row_handler:
                    self.post_row_handler(obj)
            if debug:
                break
        if self.post_import_handler and save:
            self.post_import_handler()
        end = datetime.now()
        sys.stdout.write(
            '{} ... {}/{}  Done in {} min  \n'.format(
                self.model._meta.label_lower, index, row_count,
                (end - start).seconds / 60))

    @property
    def df(self):
        """Returns a dataframe from the CSV.
        """
        def date_parser(x):
            """Func to convert date/datetime string to timezone aware datetime.
            """
            if pd.isnull(x):
                return np.nan
            if re.match('^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$', x):
                dt = datetime.strptime(x, '%Y-%m-%d')
            elif re.match('^[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}\:[0-9]{2}\:[0-9]{2}$', x):
                dt = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
            elif re.match('^[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}\:[0-9]{2}\:[0-9]{2}\+[0-9]{2}\:[0-9]{2}$', x):
                x = re.match(
                    '^[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}\:[0-9]{2}\:[0-9]{2}', x).group()
                dt = datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
            else:
                raise ImportDataError('Invalid date string. Got {}'.format(x))
            return arrow.Arrow.fromdatetime(dt).to('UTC').datetime

        if self._df.empty:
            df = pd.read_csv(self.path, low_memory=False)
            parse_dates = self.date_columns(df)
            self._df = pd.read_csv(
                self.path, low_memory=False,
                parse_dates=parse_dates, date_parser=date_parser)
            self._df = self._df.rename(columns=self.df_rename_columns)
            for column_name in self.df_drop_columns:
                self._df = self._df.drop(column_name, axis=1)
            for column, options in self.df_map_options.items():
                self._df[column] = self._df[column].map(options.get)
            for column, func in self.df_apply_functions.items():
                self._df[column] = self._df.apply(
                    lambda row: func(row), axis=1)

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

    def validate_choice_fields(self, row):
        for field, value in row.items():
            if value:
                try:
                    choices = self.choice_fields[field]
                except KeyError:
                    pass
                else:
                    if value not in [c[0] for c in choices]:
                        raise ImportError(
                            'Invalid choice for field {}. Expected one of {}. '
                            'Got {}.'.format(
                                field, [c[0] for c in choices], value))
