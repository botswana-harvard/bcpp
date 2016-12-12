from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

from edc_base.model.models import HistoricalRecords
from edc_base.model.fields import OtherCharField
from edc_base.model.validators import datetime_not_future
from edc_constants.choices import YES_NO, PIMA

from .model_mixins import CrfModelMixin


class Pima (CrfModelMixin):

    pima_today = models.CharField(
        verbose_name="Was a PIMA CD4 done today?",
        choices=YES_NO,
        max_length=3,
        help_text="",
    )

    pima_today_other = models.CharField(
        verbose_name="If no PIMA CD4 today, please explain why",
        max_length=50,
        choices=PIMA,
        null=True,
        blank=True,
    )

    pima_today_other_other = OtherCharField()

    pima_id = models.CharField(
        verbose_name="PIMA CD4 machine ID?",
        max_length=9,
        validators=[RegexValidator(regex='\d+', message='PIMA ID must be a two digit number.')],
        null=True,
        blank=True,
        help_text="type this id directly from the machine as labeled")

    cd4_datetime = models.DateTimeField(
        verbose_name="PIMA CD4 Date and time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    cd4_value = models.DecimalField(
        verbose_name="PIMA CD4 count",
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        help_text="",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "PIMA CD4 count"
        verbose_name_plural = "PIMA CD4 count"
