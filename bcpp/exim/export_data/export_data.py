import os


from edc_pdutils import ExportDataToCsv


class ExportData(ExportDataToCsv):

    def __init__(self, path_root=None, **kwargs):
        kwargs.update(export_csv=False)
        super().__init(**kwargs)
        self.path_root = path_root or '/Users/erikvw/bcpp_201703'
        self.make_folders()

    def make_folders(self):
        """mkdir a folder for each app that has models relative to path.
        """
        # build folder structure for CSV files
        for models in [self.unencrypted_models, self.encrypted_models]:
            paths = []
            for model in models:
                path_or_buf = os.path.join(
                    self.path_root, model._meta.app_label)
                paths.append(path_or_buf)
            paths = list(set(paths))
            for p in paths:
                try:
                    os.mkdir(p)
                except OSError:
                    pass

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
            self.export_model_to_csv(model, overwrite_csv=overwrite_csv)
