from django.db import models

from edc_base.model.fields import OtherCharField
from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO_UNSURE, YES_NO

from ..choices import COMMUNITY_NA

from .model_mixins import CrfModelMixin, CrfModelManager, CircumcisionMixin


class Circumcision (CircumcisionMixin, CrfModelMixin):

    circumcised = models.CharField(
        verbose_name="Are you circumcised?",
        max_length=15,
        choices=YES_NO_UNSURE,
        help_text="")

    last_seen_circumcised = models.CharField(
        verbose_name="Since we last spoke with you on last_seen_circumcised, have you been circumcised?",
        max_length=15,
        null=True,
        blank=True,
        choices=YES_NO,
        help_text="")

    circumcised_datetime = models.DateField(
        verbose_name='If Yes, date?',
        default=None,
        null=True,
        blank=True,
        help_text=""
    )

    circumcised_location = models.CharField(
        verbose_name="IF YES, Location?",
        max_length=25,
        choices=COMMUNITY_NA,
        null=True,
        blank=True,
        help_text="")

    circumcised_location_other = OtherCharField()

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Circumcision"
        verbose_name_plural = "Circumcision"
