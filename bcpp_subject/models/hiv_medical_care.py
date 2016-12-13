from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.validators import date_not_future

from ..choices import LOWEST_CD4_CHOICE

from .model_mixins import CrfModelMixin


class HivMedicalCare (CrfModelMixin):

    first_hiv_care_pos = models.DateField(
        verbose_name="When did you first receive HIV-related medical care "
                     "for such things as a CD4 count (masole), IDCC/ PMTCT "
                     "registration, additional clinic-based counseling?",
        validators=[date_not_future],
        max_length=25,
        null=True,
        blank=True,
        help_text="Note: If participant does not want to answer, leave blank.  "
                  "If participant is unable to estimate date, leave blank.",
    )

    last_hiv_care_pos = models.DateField(
        verbose_name="When did you last (most recently) receive HIV-related "
                     "medical care for such things as a CD4 count (masole), "
                     "IDCC/ PMTCT registration, additional clinic-based counseling?",
        validators=[date_not_future],
        max_length=25,
        null=True,
        blank=True,
        help_text="Note: If participant does not want to answer,leave blank. "
                  "If participant is unable to estimate date, leave blank.",
    )

    lowest_cd4 = models.CharField(
        verbose_name="What was your lowest CD4 (masole) count that was ever measured?",
        max_length=25,
        choices=LOWEST_CD4_CHOICE,
        help_text="Assist the participant by helping review their outpatient cards if "
                  "they are available.",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "HIV Medical care"
        verbose_name_plural = "HIV Medical care"
