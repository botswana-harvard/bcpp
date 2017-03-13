import sys

from collections import OrderedDict
from datetime import datetime
from pprint import pprint

from django.core.management.color import color_style
from django.db import transaction
from django.db.utils import IntegrityError

from .base_import_csv import BaseImportCsv

style = color_style()


class ImportCsvToModel(BaseImportCsv):

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

    def __init__(self, save=None, debug=None, **kwargs):
        super().__init__(**kwargs)
        self._choice_fields = {}
        self.model = kwargs.get('recipe').model
        self.populate(save=save, debug=debug)

    def populate(self, save=None, debug=None):
        start = datetime.now()
        sys.stdout.write('{} ...\r'.format(self.model._meta.label_lower))
        row_count = len(self.df)
        error_count = 0
        rows = (OrderedDict(row) for i, row in self.df.iterrows())
        for index, row in enumerate(rows):
            sys.stdout.write(
                '{} ...{}/{}  \r'.format(self.model._meta.label_lower, index + 1, row_count))
            if debug:
                pprint(row)
            row = self.convert_nan(row)
            if self.row_handler:
                row = self.row_handler(row)
            self.validate_choice_fields(row)
            obj = self.model(**row)
            if save:
                if not self.model.objects.filter(id=obj.id).exists():
                    try:
                        with transaction.atomic():
                            obj.save_base(raw=True)
                    except IntegrityError as e:
                        err_msg = '{}. Got {}'.format(str(e), obj.id)
                        if self.raise_errors:
                            pprint(obj.__dict__)
                            raise IntegrityError(err_msg)
                        else:
                            sys.stdout.write(
                                style.ERROR('\n' + err_msg + '\n'))
                            error_count += 1
                    if self.post_row_handler:
                        self.post_row_handler(obj)
            if debug:
                break
        if self.post_import_handler and save:
            self.post_import_handler()
        end = datetime.now()
        sys.stdout.write(
            '{} ... {}/{}.  {}. Done in {} min  \n'.format(
                self.model._meta.label_lower, index +
                1, row_count,
                '{} error{}'.format(
                    error_count, 's' if error_count > 1 else ''),
                (end - start).seconds / 60))

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
