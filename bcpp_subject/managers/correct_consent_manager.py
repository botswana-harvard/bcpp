from django.apps import apps as django_apps
from django.db import models


class CorrectConsentManager(models.Manager):

    def get_by_natural_key(self, report_datetime, subject_identifier_as_pk):
        SubjectConsent = django_apps.get_model('bcpp_subject', 'SubjectConsent')
        subject_consent = SubjectConsent.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(report_datetime=report_datetime, subject_consent=subject_consent)
