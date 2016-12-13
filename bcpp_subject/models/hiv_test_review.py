from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.validators import date_not_future

from edc_constants.choices import POS_NEG_IND_UNKNOWN

from .model_mixins import CrfModelMixin


class HivTestReview (CrfModelMixin):

    """Complete this form if HivTestingHistory.has_record."""

    hiv_test_date = models.DateField(
        verbose_name="What was the recorded date of the last HIV test?",
        validators=[date_not_future],
        help_text="Obtain this information from the card the participant presents to you.",
    )

    recorded_hiv_result = models.CharField(
        verbose_name="What was the recorded HIV test result?",
        max_length=30,
        choices=POS_NEG_IND_UNKNOWN,
        help_text="If the participant and written record differ, the result"
                  " from the written record should be recorded.",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "HIV Test Review"
        verbose_name_plural = "HIV Test Review"
