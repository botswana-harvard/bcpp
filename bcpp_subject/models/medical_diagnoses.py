from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO_DWTA

from .list_models import Diagnoses
from .model_mixins import CrfModelMixin


class MedicalDiagnoses (CrfModelMixin):

    """A model completed by the user to record any major illnesses in the past 12 months."""

    diagnoses = models.ManyToManyField(
        Diagnoses,
        verbose_name="Do you recall or is there a record of having any of the"
                     " following serious illnesses?",
        help_text="tick all that apply",
    )

    heart_attack_record = models.CharField(
        verbose_name="Is a record (OPD card, discharge summary) of a heart disease or stroke"
                     " diagnosis available to review?",
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
        help_text="Please review the available OPD card or other medical records, for all participants",
    )

    cancer_record = models.CharField(
        verbose_name="Is a record (OPD card, discharge summary) of a cancer diagnosis"
                     " available to review?",
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
        help_text="Please review the available OPD card or other medical records, for all participants",
    )

    tb_record = models.CharField(
        verbose_name="Is a record (OPD card, discharge summary, TB card) of a tuberculosis"
                     " infection available to review?",
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
        help_text="Please review the available OPD card or other medical records, for all participants",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Medical Diagnoses"
        verbose_name_plural = "Medical Diagnoses"
