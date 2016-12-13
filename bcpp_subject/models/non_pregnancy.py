from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO_UNSURE

from .model_mixins import CrfModelMixin, PregnancyMixin


class NonPregnancy (PregnancyMixin, CrfModelMixin):

    """A model completed by the user for female participants who are not pregnant."""

    more_children = models.CharField(
        verbose_name="Do you wish to have a child now or in the future?",
        max_length=25,
        choices=YES_NO_UNSURE,
        help_text="",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Non Pregnancy"
        verbose_name_plural = "Non Pregnancy"
