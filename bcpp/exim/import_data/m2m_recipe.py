import os
import pandas as pd
import sys

from django.apps import apps as django_apps
from django.db import connection

from .import_csv_to_model import ImportCsvToModel
from .model_recipe import ModelRecipe
from .recipe import Recipe
from .settings import OLD_DB, NEW_DB, SOURCE_DIR, UPDATED_DIR
from django.db.utils import OperationalError


class M2MImportError(Exception):
    pass


class M2mRecipe(Recipe):

    def __init__(self, field_name=None, data_model_name=None, old_list_model_name=None,
                 list_model_name=None, old_data_model_app_label=None,
                 old_data_model_model_name=None,
                 join_lists_on=None, read_sep=None, write_sep=None, **kwargs):
        super().__init__(**kwargs)
        self._list_df = pd.DataFrame()
        self._new_list_df = pd.DataFrame()
        self._old_list_df = pd.DataFrame()
        self._lists_sql = None
        self.read_sep = read_sep or '|'
        self.write_sep = write_sep or '|'
        self.field_name = field_name
        self.list_fields = [
            'created',
            'modified',
            'user_created',
            'user_modified',
            'hostname_created',
            'hostname_modified',
            'revision',
            'id',
            'name',
            'short_name',
            'display_index',
            'field_name',
            'version']
        self.join_lists_on = join_lists_on or 'short_name'
        self.data_model = django_apps.get_model(*data_model_name.split('.'))
        self.old_data_model_app_label = old_data_model_app_label
        self.old_data_model_model_name = old_data_model_model_name
        self.list_model = django_apps.get_model(*list_model_name.split('.'))
        self.old_list_model_name = old_list_model_name
        self.name = '{}.{}'.format(
            self.data_model._meta.label_lower, self.list_model._meta.model_name)

    def run(self):
        self.import_list_model()
        outfile = self.old_intermediate_into_outfile()
        infile = self.update_intermediate_into_infile(outfile)
        self.load_intermediate_infile(infile)

    @property
    def old_list_df(self):
        """Returns a DF of the original list.
        """
        if self._old_list_df.empty:
            path = os.path.join(
                SOURCE_DIR, self.old_list_model_name.split('.')[0],
                '{}.csv'.format(self.old_list_model_name.split('.')[1]))
            sys.stdout.write(
                '  M2M, importing old list model from {}'.format(path))
            df = pd.read_csv(
                path, low_memory=False,
                encoding='utf-8',
                sep=',')
            if len(list(df.columns)) == 1:
                df = pd.read_csv(
                    path, low_memory=False,
                    encoding='utf-8',
                    sep='|',
                    lineterminator='\n',
                    escapechar='\\')
            try:
                df['short_name'] = df.apply(
                    self.df_apply_functions['short_name'], axis=1)
            except KeyError:
                pass
            self._old_list_df = df
        return self._old_list_df

    @property
    def new_list_df(self):
        """Returns a DF of the new list.
        """
        if self._new_list_df.empty:
            sql = 'SELECT {fields} FROM {db}.{list_dbtable}'.format(
                db=NEW_DB, list_dbtable=self.list_model._meta.db_table,
                fields=','.join(self.list_fields))
            with connection.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
            data = {}
            for index, field in enumerate(self.list_fields):
                data.update({field: [row[index] for row in rows]})
            self._new_list_df = pd.DataFrame(data)
        return self._new_list_df

    @property
    def list_df(self):
        """Returns a DF that is a merge of the old and new list dfs (to link old and new id).
        """
        df = pd.merge(self.old_list_df, self.new_list_df,
                      on='short_name', how='left', suffixes=['_old', ''])
        if not len(df[pd.isnull(df['id'])]) == 0:
            raise M2MImportError('Some M2M options do not match.')
        return df

    def import_list_model(self):
        """Exports then re-imports list data after updating id to a UUID.
        """
        path = os.path.join(
            UPDATED_DIR, self.list_model._meta.app_label,
            '{}.csv'.format(self.list_model._meta.model_name))
        self.list_df.to_csv(
            columns=self.list_fields,
            path_or_buf=path,
            index=False,
            encoding='utf-8',
            sep='|',
            line_terminator='\n',
            escapechar='\\')
        recipe = ModelRecipe(model_name=self.list_model._meta.label_lower)
        recipe.in_path = path
        ImportCsvToModel(recipe=recipe, save=True)

    @property
    def old_intermediate_tblname(self):
        """Returns the db.tablename.
        """
        return '{}.{}_{}_{}'.format(
            OLD_DB,
            self.old_data_model_app_label,
            self.old_data_model_model_name or self.data_model._meta.model_name,
            self.field_name)

    @property
    def intermediate_tblname(self):
        """Returns the db.tablename.
        """
        return '{}.{}_{}_{}'.format(
            NEW_DB,
            self.data_model._meta.app_label,
            self.data_model._meta.model_name,
            self.field_name)

    def old_intermediate_into_outfile(self):
        """Exports the original intermediate data into an OUTFILE.
        """
        tbl = self.old_intermediate_tblname
        outfile = os.path.join(
            UPDATED_DIR, '{}_{}.outfile.txt'.format(
                '/'.join(self.data_model._meta.label_lower.split('.')),
                self.list_model._meta.model_name))
        sql = (
            "SELECT 'id', '{data_field}', '{field_name}' "
            "UNION ALL "
            "SELECT id, replace({data_field}, '-', ''), {field_name} INTO OUTFILE "
            "'{outfile}' "
            "CHARACTER SET UTF8 "
            "FIELDS TERMINATED BY '|' ENCLOSED BY '' "
            "LINES TERMINATED BY '\n' "
            "FROM {tbl};").format(
                data_field='{}_id'.format(self.old_data_model_model_name),
                field_name='{}_id'.format(
                    self.old_list_model_name.split('.')[1]),
                outfile=outfile, tbl=tbl)
        with connection.cursor() as cursor:
            cursor.execute(sql)
        return outfile

    def update_intermediate_into_infile(self, outfile=None):
        """Reads the OUTFILE, updates the ids, writes back to INFILE.
        """
        infile = outfile.replace('outfile', 'infile')
        list_field = '{}_id'.format(self.list_model._meta.model_name)
        df = pd.read_csv(outfile, low_memory=False, sep=self.read_sep)
        columns = list(df.columns)
        if list_field not in columns:
            raise M2MImportError(
                'Invalid list field for intermediate table. Got {}. '
                'Expected one of {}'.format(list_field, columns))
        df = pd.merge(
            df, self.list_df, left_on=list_field, right_on='id_old', suffixes=['', '_new'])
        df = df.drop([list_field], axis=1)
        df = df.rename(columns={'id_new': list_field})
        df.to_csv(
            columns=columns,
            path_or_buf=infile,
            index=False,
            encoding='utf-8',
            sep=self.write_sep,
            line_terminator='\n',
            escapechar='\\')
        return infile

    def load_intermediate_infile(self, infile=None):
        """Loads the updated INFILE to the new DB intermediate table.
        """
        tbl = self.intermediate_tblname
        sql = (
            "LOAD DATA INFILE '{infile}' INTO TABLE {tbl} "
            "CHARACTER SET UTF8 "
            "FIELDS TERMINATED BY '|' ENCLOSED BY '' "
            "LINES TERMINATED BY '\n' "
            "IGNORE 1 LINES "
            "(id, {data_field}, {list_field});".format(
                data_field='{}_id'.format(self.data_model._meta.model_name),
                list_field='{}_id'.format(self.list_model._meta.model_name),
                infile=infile, tbl=tbl))
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
            "FIELDS TERMINATED BY '|' ENCLOSED BY '' "
            "LINES TERMINATED BY '\n' "
            "FROM {old_db}.{old_list_dbtable};").format(
                csv_filename=csv_filename, old_db=OLD_DB,
                old_list_dbtable='_'.join(self.old_list_model_name.split('.')))
        with connection.cursor() as cursor:
            cursor.execute(sql)
