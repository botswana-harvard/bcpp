from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO_NA, YES_NO_DWTA

from ..choices import WHEN_HIV_TEST_CHOICE, VERBAL_HIV_RESULT_CHOICE, YES_NO_RECORD_REFUSAL

from .model_mixins import CrfModelMixin


class HivTestingHistory (CrfModelMixin):

    """A model completed by the user of the particiapn's history of testing for HIV."""

    has_tested = models.CharField(
        verbose_name="Have you ever been tested for HIV before?",
        max_length=25,
        choices=YES_NO_DWTA,
        help_text="",
    )

    when_hiv_test = models.CharField(
        verbose_name="When was the last [most recent]"
                     " time you were tested for HIV?",
        max_length=25,
        null=True,
        blank=True,
        choices=WHEN_HIV_TEST_CHOICE,
        help_text="(verbal response)",
    )

    # this field triggers HivTestReview
    has_record = models.CharField(
        verbose_name="Is a record of last [most recent] HIV test [OPD card, Tebelopele,"
                     " other] available to review?",
        max_length=45,
        null=True,
        blank=True,
        choices=YES_NO_RECORD_REFUSAL,
        help_text="if no card available for viewing, proceed to next question",
    )

    verbal_hiv_result = models.CharField(
        verbose_name="Please tell me the results of your last [most recent] HIV test?",
        max_length=30,
        null=True,
        blank=True,
        choices=VERBAL_HIV_RESULT_CHOICE,
        help_text="(verbal response)",
    )

    # this field triggers HivResultDocumentation
    other_record = models.CharField(
        verbose_name="Do you have any other available documentation of positive HIV status?",
        max_length=3,
        null=True,
        blank=False,
        choices=YES_NO_NA,
        default=YES_NO_NA[2][0],
        help_text="This documentation refers to: PMTCT prescription, ART, CD4 count record, lab result for.. etc",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "HIV Testing History"
        verbose_name_plural = "HIV Testing History"
