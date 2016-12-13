from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from edc_base.model.models import HistoricalRecords
from edc_base.model.validators import datetime_not_future
from edc_constants.choices import YES_NO

from .model_mixins import CrfModelMixin, CrfModelManager


class Cd4History (CrfModelMixin):

    """CS002 - used to collect participant CD4 History"""

    record_available = models.CharField(
        verbose_name="Is record of last CD4 count available?",
        max_length=3,
        choices=YES_NO,
        help_text="")

    last_cd4_count = models.DecimalField(
        verbose_name="What is the value of the last 'CD4' test recorded?",
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(3000)],
        null=True,
        blank=True,
        help_text="")

    last_cd4_drawn_date = models.DateField(
        verbose_name="Date last 'CD4' test was run",
        validators=[
            datetime_not_future, ],
        null=True,
        blank=True,
        help_text="")

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "CD4 History"
        verbose_name_plural = "CD4 History"
