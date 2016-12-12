from django.db.models import get_app, get_models
from django.test import TestCase

from ..models import SubjectConsent, SubjectVisit


class TestOffStudy(TestCase):
    app_label = 'bcpp_subject'
    subject_consent = SubjectConsent
    consent_catalogue_name = 'v1'
    visit_model = SubjectVisit

    def test_has_off_study_mixin(self):
        app = get_app(self.app_label)
        for model in get_models(app):
            if 'Audit' not in model._meta.object_name and 'OffStudy' not in model._meta.object_name:
                if model._meta.model_name in ['subjectoffstudy']:
                    self.assertTrue(
                        'off_study_model' in dir(model),
                        'Method \'off_study_model\' not found on model {0}'.format(model._meta.object_name))
                    self.assertTrue(
                        'is_off_study' in dir(model),
                        'Method \'is_off_study\' not found on model {0}'.format(model._meta.object_name))
                    self.assertTrue(
                        'get_report_datetime' in dir(model),
                        'Method \'get_report_datetime\' not found on model {0}'.format(model._meta.object_name))
                    self.assertTrue(
                        'get_subject_identifier' in dir(model),
                        'Method \'get_subject_identifier\' not found on model {0}'.format(model._meta.object_name))
