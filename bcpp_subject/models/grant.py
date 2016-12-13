from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.fields import OtherCharField

from ..choices import GRANT_TYPE

from .model_mixins import CrfModelMixin
from .labour_market_wages import LabourMarketWages


class Grant(CrfModelMixin):

    """Inline for labour_market_wages."""

    labour_market_wages = models.ForeignKey(LabourMarketWages)

    grant_number = models.IntegerField(
        verbose_name="How many of each type of grant do you receive?",
        null=True,
        blank=True,
    )
    grant_type = models.CharField(
        verbose_name="Grant name",
        choices=GRANT_TYPE,
        max_length=50,
        null=True,
        blank=True)

    other_grant = OtherCharField()

    history = HistoricalRecords()

    def __str__(self):
        return str(self.labour_market_wages.subject_visit)

    def natural_key(self):
        return (self.report_datetime, ) + self.labour_market_wages.natural_key()
    natural_key.dependencies = ['bcpp_subject.labourmarketwages', ]

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Grant"
        verbose_name_plural = "Grants"
