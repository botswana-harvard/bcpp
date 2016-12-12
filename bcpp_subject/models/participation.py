from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO

from ..choices import PARTIAL_PARTICIPATION_TYPE

from .model_mixins import CrfModelMixin


class Participation (CrfModelMixin):

    full = models.CharField(
        verbose_name='Has the participant agreed to fully participate in BHS',
        max_length=15,
        choices=YES_NO,
        default='Yes',
    )

    participation_type = models.CharField(
        verbose_name="What type of partial participation did the client choose?",
        max_length=30,
        choices=PARTIAL_PARTICIPATION_TYPE,
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name = "Participation"
        verbose_name_plural = "Participation"
