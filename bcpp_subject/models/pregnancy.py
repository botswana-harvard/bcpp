from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.validators import date_not_future

from ..choices import ANC_REG_CHOICE

from .model_mixins import CrfModelMixin, PregnancyMixin


class Pregnancy (PregnancyMixin, CrfModelMixin):

    """A model completed by the user for pregnant participants."""

    anc_reg = models.CharField(
        verbose_name="Have you registered for antenatal care?",
        max_length=55,
        null=True,
        blank=True,
        choices=ANC_REG_CHOICE,
        help_text="",
    )

    lnmp = models.DateField(
        verbose_name="When was the first day of your last normal menstrual period?",
        validators=[date_not_future],
        help_text="",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Pregnancy"
        verbose_name_plural = "Pregnancy"
