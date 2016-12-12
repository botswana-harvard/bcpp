from django.db import models

from bcpp.models import RegisteredSubject
from edc_base.model.models import BaseUuidModel, HistoricalRecords

from bcpp_household_member.models import HouseholdMember
from bcpp_survey.models import Survey

from ..managers import ConsentHistoryManager


class SubjectConsentHistory(BaseUuidModel):

    survey = models.ForeignKey(Survey)

    household_member = models.ForeignKey(HouseholdMember)

    registered_subject = models.ForeignKey(RegisteredSubject)
    consent_datetime = models.DateTimeField()
    consent_pk = models.CharField(max_length=50)
    consent_app_label = models.CharField(max_length=50)
    consent_model_name = models.CharField(max_length=50)

    objects = ConsentHistoryManager()

    history = HistoricalRecords()

    def natural_key(self):
        if not self.registered_subject:
            raise AttributeError("registered_subject cannot be None for pk='\{0}\'".format(self.pk))
        return self.consent_datetime + self.survey + self.registered_subject.natural_key()
    natural_key.dependencies = ['registration.registered_subject']

    class Meta:
        app_label = 'bcpp_subject'
