from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.validators import datetime_not_future
from edc_constants.choices import POS_NEG

from .hic_enrollment import HicEnrollment
from .model_mixins import CrfModelMixin


class ElisaHivResult (CrfModelMixin):

    hiv_result = models.CharField(
        verbose_name="HIV test result from the Elisa",
        max_length=50,
        choices=POS_NEG,
    )

    hiv_result_datetime = models.DateTimeField(
        verbose_name="HIV test result from the Elisa date and time",
        null=True,
        blank=True,
        validators=[datetime_not_future],
    )

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.hic_enrollment_checks()
        self.elisa_requisition_checks()
        super(ElisaHivResult, self).save(*args, **kwargs)

    def hic_enrollment_checks(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        if HicEnrollment.objects.filter(subject_visit=self.subject_visit).exists():
            if self.hiv_result.lower() != 'neg':
                raise exception_cls('Result cannot be changed. HIC Enrollment form exists '
                                    'for this subject. Got {0}'.format(self.hiv_result))

    def elisa_requisition_checks(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        SubjectRequisition = django_apps.get_model('bcpp_lab', 'SubjectRequisition')
        if not SubjectRequisition.objects.filter(subject_visit=self.subject_visit, panel__name='ELISA').exists():
            raise exception_cls('ELISA Result cannot be saved before an ELISA Requisition is requested.')

    class Meta(CrfModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name = "Elisa\'s HIV Result"
        verbose_name_plural = "Elisa\'s HIV Result"
