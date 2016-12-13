from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.validators import date_not_future
from edc_constants.choices import POS_NEG_UNKNOWN
from edc_constants.constants import POS

from ..choices import HIV_DOC_TYPE

from .model_mixins import CrfModelMixin


class HivResultDocumentation (CrfModelMixin):

    # base on question from hiv test history
    result_date = models.DateField(
        verbose_name='What is the recorded date of this previous HIV test (or of the '
                     'document that provides supporting evidence of HIV infection)?',
        validators=[date_not_future],
        help_text="",
    )

    result_recorded = models.CharField(
        verbose_name='What is the recorded HIV status indicated by this additional document?',
        max_length=30,
        choices=POS_NEG_UNKNOWN,  # this is always POSITIVE!!
        default=POS,
        help_text=('value should always be POS as the rule group only shows this form '
                   'if verbal_hiv_result is POS and have indirect documentation.'),
        editable=False,
    )

    result_doc_type = models.CharField(
        verbose_name="What is the type of document used?",
        max_length=35,
        choices=HIV_DOC_TYPE,
        help_text="",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "HIV result documentation"
        verbose_name_plural = "HIV result documentation"
