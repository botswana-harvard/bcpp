from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.fields import OtherCharField
from edc_base.model.validators import date_not_future

from .list_models import HeartDisease
from .model_mixins import CrfModelMixin


class HeartAttack (CrfModelMixin):

    """A model completed by the user to record any heart conditions in the past 12 months."""

    date_heart_attack = models.DateField(
        verbose_name="Date of the heart disease or stroke diagnosis:",
        validators=[date_not_future],
        help_text="",
    )

    dx_heart_attack = models.ManyToManyField(
        HeartDisease,
        verbose_name="[Interviewer:] What is the heart disease or stroke diagnosis as recorded?",
        help_text=("(tick all that apply)"),
    )

    dx_heart_attack_other = OtherCharField()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Heart Attack or Stroke"
        verbose_name_plural = "Heart Attack or Stroke"
