from edc_appointment.model_mixins import AppointmentModelMixin, AppointmentManager
from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_consent.model_mixins import RequiresConsentMixin


class Appointment(AppointmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    objects = AppointmentManager()

    history = HistoricalRecords()

    class Meta(AppointmentModelMixin.Meta):
        consent_model = 'bcpp_subject.subjectconsent'
        app_label = 'bcpp_subject'
