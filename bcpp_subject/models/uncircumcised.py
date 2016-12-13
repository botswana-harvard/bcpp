from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.fields import OtherCharField
from edc_constants.choices import YES_NO_DWTA, YES_NO_UNSURE

from ..choices import REASON_CIRC_CHOICE, FUTURE_REASONS_SMC_CHOICE, AWARE_FREE_CHOICE

from .model_mixins import CircumcisionMixin, CrfModelMixin


class Uncircumcised (CircumcisionMixin, CrfModelMixin):

    reason_circ = models.CharField(
        verbose_name="What is the main reason that you have not yet been circumcised?",
        max_length=65,
        null=True,
        choices=REASON_CIRC_CHOICE,
        help_text="",
    )

    reason_circ_other = OtherCharField(
        null=True,)

    future_circ = models.CharField(
        verbose_name="Would you ever consider being circumcised in the future?",
        max_length=25,
        choices=YES_NO_UNSURE,
        help_text="",
    )

    future_reasons_smc = models.CharField(
        verbose_name="Which of the following might increase your willingness to"
                     " be circumcised the most?",
        max_length=75,
        choices=FUTURE_REASONS_SMC_CHOICE,
        null=True,
        help_text="",
    )

    service_facilities = models.CharField(
        verbose_name="Were you aware that circumcision services are provided "
                     "free of charge at most health facilities?",
        max_length=35,
        choices=YES_NO_DWTA,
        null=True,
        help_text="",
    )

    aware_free = models.CharField(
        verbose_name="Where did you learn that circumcision services were "
                     "available free at most health facilities?",
        max_length=85,
        null=True,
        blank=True,
        choices=AWARE_FREE_CHOICE,
        help_text="",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Uncircumcised"
        verbose_name_plural = "Uncircumcised"
