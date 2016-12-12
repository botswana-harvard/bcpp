
from datetime import timedelta
from django.apps import apps as django_apps
from django.core.exceptions import MultipleObjectsReturned
from django.db import models


class ConsentHistoryManager(models.Manager):

    def get_by_natural_key(self, consent_datetime, survey_name, subject_identifier_as_pk):
        margin = timedelta(minutes=5)
        RegisteredSubject = django_apps.get_model('registration', 'RegisteredSubject')
        Survey = django_apps.get_model('bcpp_survey', 'Survey')
        survey = Survey.objects.get_by_natural_key(survey_name)
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(consent_datetime__range=(
            consent_datetime - margin, consent_datetime + margin), survey=survey, registered_subject=registered_subject)

    def update_consent_history(self, consent_inst, created, using):
        try:
            inst = self.get(
                registered_subject=consent_inst.registered_subject,
                consent_app_label=consent_inst._meta.app_label,
                consent_model_name=consent_inst._meta.object_name,
                consent_pk=consent_inst.pk)
            inst.consent_datetime = consent_inst.consent_datetime
            inst.save(using=using)
        except MultipleObjectsReturned:
            # not sure why this is happening????
            inst = self.filter(
                registered_subject=consent_inst.registered_subject,
                consent_app_label=consent_inst._meta.app_label,
                consent_model_name=consent_inst._meta.object_name,
                consent_pk=consent_inst.pk).order_by('-created')[0]
            inst.consent_datetime = consent_inst.consent_datetime
            inst.save(using=using)
        except self.model.DoesNotExist:
            self.create(
                registered_subject=consent_inst.registered_subject,
                consent_app_label=consent_inst._meta.app_label,
                consent_model_name=consent_inst._meta.object_name,
                consent_pk=consent_inst.pk,
                survey=consent_inst.survey,
                household_member=consent_inst.household_member,
                consent_datetime=consent_inst.consent_datetime)

    def delete_consent_history(self, app_label, model_name, pk, using):
        super(ConsentHistoryManager, self).filter(
            consent_app_label=app_label, consent_model_name=model_name, consent_pk=pk).delete()
