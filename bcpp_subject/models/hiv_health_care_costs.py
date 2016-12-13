from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO_REFUSED

from ..choices import NO_MEDICALCARE_REASON, HEALTH_CARE_PLACE, CARE_REGULARITY, DOCTOR_VISITS

from .model_mixins import CrfModelMixin


class HivHealthCareCosts (CrfModelMixin):

    """A model completed by the user to capture information from the
    participant about obtaining medical or clinical care related to HIV."""

    hiv_medical_care = models.CharField(
        verbose_name="Have you ever received HIV related medical/clinical care? ",
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text="",
    )
    reason_no_care = models.CharField(
        verbose_name="If you have never received HIV related medical/clinical care, why not? ",
        max_length=115,
        null=True,
        blank=True,
        choices=NO_MEDICALCARE_REASON,
        help_text="",
    )
    place_care_received = models.CharField(
        verbose_name="Where do you receive most of your HIV related health care? ",
        max_length=40,
        default='None',
        null=True,
        blank=False,
        choices=HEALTH_CARE_PLACE,
        help_text="",
    )
    care_regularity = models.CharField(
        verbose_name="In the past 3 months, how many times did you have clinic visits to see a health care worker,"
                     " a nurse, or doctor? ",
        max_length=20,
        choices=CARE_REGULARITY,
        null=True,
        blank=False,
        default='0 times',
        help_text="Do not include medicine re-fill visits.",
    )
    doctor_visits = models.CharField(
        verbose_name="In the last 3 months, how often did someone take you to the doctor? ",
        max_length=32,
        choices=DOCTOR_VISITS,
        null=True,
        blank=False,
        default='never',
        help_text="",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "HIV health care costs"
        verbose_name_plural = "HIV health care costs"
