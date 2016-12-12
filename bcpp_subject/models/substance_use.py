from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO_DWTA

from ..choices import ALCOHOL_CHOICE

from .model_mixins import CrfModelMixin


class SubstanceUse(CrfModelMixin):

    alcohol = models.CharField(
        verbose_name="In the past month, how often did you consume alcohol?",
        max_length=25,
        choices=ALCOHOL_CHOICE,
        help_text="If participant does not know exactly, ask to give a best guess.",
    )

    smoke = models.CharField(
        verbose_name="Do you currently smoke any tobacco products, such as cigarettes, cigars, or pipes?",
        max_length=25,
        choices=YES_NO_DWTA,
        help_text="",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Substance Use"
        verbose_name_plural = "Substance Use"
