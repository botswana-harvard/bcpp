import os

from .import_csv_to_table import ImportCsvToTable
from .recipe import Recipe


class TableRecipe(Recipe):

    import_csv_class = ImportCsvToTable

    def __init__(self, table_name=None, csv_subfolder=None, **kwargs):
        super().__init__(**kwargs)
        self.name = table_name
        self.table_name = table_name
        csv_filename = self.csv_filename or '{}.csv'.format(table_name)
        self.path = os.path.join(
            self.csv_folder, csv_subfolder or '', csv_filename)
