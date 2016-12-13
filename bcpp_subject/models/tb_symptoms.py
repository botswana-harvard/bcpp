from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO

from .model_mixins import CrfModelMixin


class TbSymptoms (CrfModelMixin):

    cough = models.CharField(
        verbose_name="Does the participant currently have a COUGH that has lasted for more than 2 weeks?",
        max_length=10,
        choices=YES_NO,
        help_text="",
    )

    fever = models.CharField(
        verbose_name="In the last two weeks has the participant had FEVER?",
        max_length=10,
        choices=YES_NO,
        help_text="",
    )

    lymph_nodes = models.CharField(
        verbose_name="Does the participant currently have ENLARGED LYMPH NODES?",
        max_length=10,
        choices=YES_NO,
        help_text="",
    )

    cough_blood = models.CharField(
        verbose_name="In the last two weeks has the participant COUGHED UP BLOOD?",
        max_length=10,
        choices=YES_NO,
        help_text="",
    )

    night_sweat = models.CharField(
        verbose_name="In the last two weeks has the participant had NIGHT SWEATS?",
        max_length=10,
        choices=YES_NO,
        help_text="",
    )

    weight_loss = models.CharField(
        verbose_name="In the last month has the participant had unexplained WEIGHT LOSS?",
        max_length=10,
        choices=YES_NO,
        help_text="",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "TB Symptoms"
        verbose_name_plural = "TB Symptoms"
