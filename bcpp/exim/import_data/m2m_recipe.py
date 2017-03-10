import pandas as pd
import re
import os

from django.apps import apps as django_apps
from django.db import connection

from .exceptions import ImportDataError
from .import_csv_to_model import ImportCsvToModel
from .model_recipe import ModelRecipe
from .recipe import Recipe
from .settings import OLD_DB, NEW_DB, SOURCE_DIR, UPDATED_DIR


class M2mRecipe(Recipe):

    def __init__(self, data_model_name=None, old_list_model_name=None,
                 list_model_name=None, old_data_model_app_label=None, **kwargs):
        super().__init__(**kwargs)
        self.data_model = django_apps.get_model(*data_model_name.split('.'))
        self.old_data_model_app_label = old_data_model_app_label
        self.list_model = django_apps.get_model(*list_model_name.split('.'))
        self.old_list_model_name = old_list_model_name
        self.name = '{}.{}'.format(
            self.data_model._meta.label_lower, self.list_model._meta.model_name)

    def run(self):
        self.import_list_model()
        outfile = self.old_intermediate_into_outfile()
        infile = self.update_intermediate_into_infile(outfile)
        self.load_intermediate_infile(infile)

    def import_list_model(self):
        """Imports list data after updating id to a UUID.
        """
        path = os.path.join(
            SOURCE_DIR, self.old_list_model_name.split('.')[0],
            '{}.csv'.format(self.old_list_model_name.split('.')[1]))
        df = pd.read_csv(path, low_memory=False)
        df['id'] = df.apply(
            lambda row: self.get_new_id(row['id']), axis=1)
        path = os.path.join(
            UPDATED_DIR, self.list_model._meta.app_label,
            '{}.csv'.format(self.list_model._meta.model_name))
        df.to_csv(
            path_or_buf=path,
            index=False,
            encoding='utf-8')
        recipe = ModelRecipe(model_name=self.list_model._meta.label_lower)
        ImportCsvToModel(recipe=recipe, save=True)

    def ids(self):
        """Returns a dictionary {old_id1: new_uuid1, old_id2: new_uuid2, ...}.
        """
        sql = (
            'SELECT old.id old_id, new.id new_id, old.short_name '
            'FROM {old_db}.{old_list_dbtable} AS old '
            'LEFT JOIN {db}.{list_dbtable} AS new '
            'ON new.short_name=old.short_name;').format(
                old_db=OLD_DB, old_list_dbtable='_'.join(
                    self.old_list_model_name.split('.')),
                db=NEW_DB, list_dbtable=self.list_model._meta.db_table)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows}

    def old_intermediate_into_outfile(self):
        """Selects the original intermediate data into an OUTFILE.
        """
        tbl = '{}_{}_{}'.format(
            self.old_data_model_app_label,
            self.data_model._meta.model_name,
            '_'.join(re.findall('[A-Z][^A-Z]*', self.list_model._meta.object_name)).lower())
        outfile = os.path.join(
            UPDATED_DIR, '{}_{}.outfile.txt'.format(
                '/'.join(self.data_model._meta.label_lower.split('.')),
                self.list_model._meta.model_name))
        sql = (
            "SELECT 'id', '{data_field}', '{list_field}' "
            "UNION ALL "
            "SELECT id, replace({data_field}, '-', ''), {list_field} INTO OUTFILE "
            "'{outfile}' "
            "CHARACTER SET UTF8 "
            "FIELDS TERMINATED BY ',' ENCLOSED BY '' "
            "LINES TERMINATED BY '\n' "
            "FROM {old_db}.{tbl};").format(
                data_field='{}_id'.format(self.data_model._meta.model_name),
                list_field='{}_id'.format(self.list_model._meta.model_name),
                outfile=outfile, old_db=OLD_DB, tbl=tbl)
        with connection.cursor() as cursor:
            cursor.execute(sql)
        return outfile

    def get_new_id(self, value):
        """Map old id to new UUID.
        """
        for old_id, new_id in self.ids.items():
            if value == old_id:
                return new_id
        raise ImportDataError(
            'M2M mapping not found. Got {}'.format(value))

    def update_intermediate_into_infile(self, outfile=None):
        """Reads the OUTFILE, updates the ids, writes back to INFILE.
        """
        infile = outfile.replace('outfile', 'infile')
        list_field = '{}_id'.format(self.list_model._meta.model_name)
        df = pd.read_csv(outfile, low_memory=False)
        df[list_field] = df.apply(
            lambda row: self.get_new_id(row[list_field]), axis=1)
        df.to_csv(
            path_or_buf=infile,
            index=False,
            encoding='utf-8')
        return infile

    def load_intermediate_infile(self, infile=None):
        """Loads the updated INFILE to the new DB intermediate table.
        """
        tbl = '{}_{}_{}'.format(
            self.data_model._meta.app_label,
            self.data_model._meta.model_name,
            '_'.join(re.findall('[A-Z][^A-Z]*', self.list_model._meta.object_name)).lower())
        sql = (
            "LOAD DATA INFILE '{infile}' INTO TABLE {db}.{tbl} "
            "CHARACTER SET UTF8 "
            "FIELDS TERMINATED BY ',' ENCLOSED BY '' "
            "LINES TERMINATED BY '\n' "
            "IGNORE 1 LINES "
            "(id, {data_field}, {list_field});".format(
                data_field='{}_id'.format(self.data_model._meta.model_name),
                list_field='{}_id'.format(self.list_model._meta.model_name),
                infile=infile, db=NEW_DB, tbl=tbl))
        with connection.cursor() as cursor:
            cursor.execute(sql)

    def export_old_list_model(self):
        """Creates a new CSV of the old list model.

        ... if for some reason it needs to be re-created ...
        """
        csv_filename = os.path.join(SOURCE_DIR, '{}.csv'.format(
            '/'.join(self.old_list_model_name.split('.'))))
        sql = (
            "SELECT 'hostname_created', 'name', 'short_name', 'created', 'user_modified', "
            "'modified', 'hostname_modified', 'version', 'display_index', 'user_created', "
            "'field_name','id','revision' "
            "UNION ALL "
            "SELECT hostname_created, name, short_name, created, user_modified, "
            "modified, hostname_modified, version, display_index, user_created, "
            "ifnull(field_name, ''),id, ifnull(revision, '') INTO OUTFILE '{csv_filename}' "
            "CHARACTER SET UTF8 "
            "FIELDS TERMINATED BY ',' ENCLOSED BY '' "
            "LINES TERMINATED BY '\n' "
            "FROM {old_db}.{old_list_dbtable};").format(
                csv_filename=csv_filename, old_db=OLD_DB,
                old_list_dbtable='_'.join(self.old_list_model_name.split('.')))
        with connection.cursor() as cursor:
            cursor.execute(sql)
