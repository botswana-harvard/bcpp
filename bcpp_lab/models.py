from django.db import models

from edc_base.model.models import BaseUuidModel, UrlMixin
from edc_consent.model_mixins import RequiresConsentMixin
from edc_lab.model_mixins import RequisitionModelMixin, AliquotModelMixin, SpecimenCollectionModelMixin
from edc_metadata.model_mixins import UpdatesRequisitionMetadataModelMixin
from edc_visit_tracking.model_mixins import CrfModelMixin

from bcpp_subject.models.subject_visit import SubjectVisit
from edc_base.model.models import HistoricalRecords
from edc_visit_tracking.managers import CrfModelManager
from edc_lab.managers import AliquotManager


class SubjectRequisition(CrfModelMixin, RequisitionModelMixin, RequiresConsentMixin,
                         UpdatesRequisitionMetadataModelMixin, UrlMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'bcpp_lab_admin'

    subject_visit = models.ForeignKey(SubjectVisit)

    objects = CrfModelManager()

    history = HistoricalRecords

    class Meta:
        app_label = 'bcpp_lab'
        consent_model = 'bcpp_subject.subjectconsent'


class Aliquot(AliquotModelMixin, BaseUuidModel):

    objects = AliquotManager()

    history = HistoricalRecords

    class Meta:
        app_label = 'bcpp_lab'
