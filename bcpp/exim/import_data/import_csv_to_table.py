import sys

from django.db import connection

from .base_import_csv import BaseImportCsv


class ImportCsvToTable(BaseImportCsv):

    def __init__(self, save=None, debug=None, **kwargs):
        super().__init__(**kwargs)
        self.table_name = kwargs.get('recipe').table_name
        self.populate(save=save, debug=debug)

    def populate(self, save=None, debug=None):
        sys.stdout.write('{} ...\r'.format(self.table_name))
        with connection.cursor() as cursor:
            cursor.execute(self.recipe.sql)
        sys.stdout.write('{} ... Done\n'.format(self.table_name))
