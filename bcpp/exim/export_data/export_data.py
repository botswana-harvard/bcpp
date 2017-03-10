import os
import sys

from django.apps import apps as django_apps
from django.db.utils import OperationalError

from edc_pdutils import ModelToDataFrame


class ExportData:

    def __init__(self, path=None):
        self.path = path or '/Users/erikvw/bcpp_201703'
        self.unencrypted_models = []
        self.encrypted_models = []
        excluded_models = [
            'incomingtransaction', 'outgoingtransaction', 'crypt']
        for app_config in django_apps.get_app_configs():
            for model in app_config.get_models():
                for field in model._meta.fields:
                    if hasattr(field, 'field_cryptor'):
                        self.encrypted_models.append(model)
                        model = None
                        break
                if model:
                    self.unencrypted_models.append(model)
        self.unencrypted_models = [
            m for m in self.unencrypted_models
            if m._meta.model_name not in excluded_models]
        self.unencrypted_models.sort(
            key=lambda x: x._meta.label_lower)
        self.encrypted_models = [
            m for m in self.encrypted_models
            if m._meta.model_name not in excluded_models]
        self.encrypted_models.sort(
            key=lambda x: x._meta.label_lower)
        self.make_folders()

    def make_folders(self):
        """mkdir a folder for each app that has models relative to path.
        """
        # build folder structure for CSV files
        for models in [self.unencrypted_models, self.encrypted_models]:
            paths = []
            for model in models:
                path_or_buf = os.path.join(
                    self.path, model._meta.app_label)
                paths.append(path_or_buf)
            paths = list(set(paths))
            for p in paths:
                try:
                    os.mkdir(p)
                except OSError:
                    pass

    def export_model_to_csv(self, model, overwrite_csv=None, encrypted=None):
        overwrite_csv = False if overwrite_csv is None else False
        msg = '{}.{}{}'.format(
            model._meta.label_lower, ' (encrypted)' if encrypted else '')
        sys.stdout.write(msg + '\r')
        count = model.objects.all().count()
        if count > 0:
            path_or_buf = os.path.join(
                self.path, model._meta.app_label,
                '{}.csv'.format(model._meta.model_name))
            if os.path.exists(path_or_buf):
                sys.stdout.write(
                    '{} exists ({} records).\n'.format(msg, count))
            if ((not os.path.exists(path_or_buf))
                    or (os.path.exists(path_or_buf) and overwrite_csv)):
                sys.stdout.write('{} creating **** \r'.format(msg))
                try:
                    m2df = ModelToDataFrame(model)
                except OperationalError as err:
                    sys.stdout.write('\nError. {}. Got {}\n\n'.format(
                        model._meta.model_name, str(err)))
                else:
                    path_or_buf = os.path.join(
                        self.path, model._meta.app_label,
                        '{}.csv'.format(model._meta.model_name))
                    m2df.dataframe.to_csv(
                        columns=m2df.columns(model.objects.all(), None),
                        path_or_buf=path_or_buf,
                        index=False,
                        encoding='utf-8')
                    sys.stdout.write('{} creating **** Done\n'.format(msg))
        else:
            sys.stdout.write('{} empty\n'.format(msg))

    def export_unencrypted(self, models=None, skip_models=None,
                           reverse=None, overwrite_csv=None):
        """Creates a CSV file for each model and places in
        path/app_label/modelname.csv.
        """
        models = models or self.unencrypted_models
        for model in models:
            self.export_model_to_csv(
                model, overwrite_csv=overwrite_csv)

    def export_encrypted(self, models=None, skip_models=None,
                         reverse=None, overwrite_csv=None):
        """Creates a CSV file for each model and places in
        path/app_label/modelname.csv.
        """
        models = models or self.encrypted_models
        if reverse:
            self.encrypted_models.reverse()
        if skip_models:
            models = [
                m for m in models if m._meta.model_name not in skip_models]
        for model in models:
            self.export_model_to_csv(
                model, overwrite_csv=overwrite_csv, encrypted=True)
