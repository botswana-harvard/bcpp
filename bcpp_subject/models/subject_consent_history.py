from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords

from member.models import HouseholdMember
from survey.models import Survey


class SubjectConsentHistory(BaseUuidModel):

    survey = models.ForeignKey(Survey)

    household_member = models.ForeignKey(HouseholdMember)

    consent_datetime = models.DateTimeField()
    consent_pk = models.CharField(max_length=50)
    consent_app_label = models.CharField(max_length=50)
    consent_model_name = models.CharField(max_length=50)

    history = HistoricalRecords()

    def natural_key(self):
        if not self.registered_subject:
            raise AttributeError("registered_subject cannot be None for pk='\{0}\'".format(self.pk))
        return self.consent_datetime + self.survey + self.registered_subject.natural_key()
    natural_key.dependencies = ['registration.registered_subject']

    class Meta:
        app_label = 'bcpp_subject'
