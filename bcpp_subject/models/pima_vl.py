from datetime import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, RegexValidator
from django_crypto_fields.fields import EncryptedTextField

from edc_base.model.fields import OtherCharField
from edc_base.model.models import HistoricalRecords
from edc_base.model.validators import datetime_not_future
from edc_constants.choices import YES_NO, PIMA
from edc_protocol.validators import datetime_not_before_study_start
from edc_quota.client.models import QuotaMixin, QuotaManager

from ..choices import EASY_OF_USE, QUANTIFIER

from .model_mixins import CrfModelMixin

PIMA_SETTING_VL = (
    ('mobile setting', 'Mobile Setting'),
    ('household setting', 'Household Setting'),
)


class PimaVl (QuotaMixin, CrfModelMixin):

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.now,  # ref: http://stackoverflow.com/questions/2771676/django-default-datetime-now-problem
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    poc_vl_type = models.CharField(
        verbose_name="Type mobile or household setting",
        choices=PIMA_SETTING_VL,
        max_length=150,
        default=PIMA_SETTING_VL[0][0],
    )

    poc_vl_today = models.CharField(
        verbose_name="Was a POC viral load done today?",
        choices=YES_NO,
        max_length=3,
        help_text="",
    )

    poc_vl_today_other = models.CharField(
        verbose_name="If no POC viral load today, please explain why",
        max_length=50,
        choices=PIMA,
        null=True,
        blank=True,
    )

    poc_today_vl_other_other = OtherCharField()

    pima_id = models.CharField(
        verbose_name="POC viral load machine ID?",
        max_length=9,
        validators=[RegexValidator(regex='\d+', message='POC viral load ID must be a two digit number.')],
        null=True,
        blank=True,
        help_text="type this id directly from the machine as labeled")

# removed
#     poc_vl_datetime = models.DateTimeField(
#         verbose_name="POC viral load Date and time",
#         validators=[datetime_not_future],
#         null=True,
#         blank=True,
#     )

    vl_value_quatifier = models.CharField(
        verbose_name="Select a quantifier for the value of the result",
        choices=QUANTIFIER,
        max_length=20,
    )

    # vl_value_quatifier_other = OtherCharField()

    poc_vl_value = models.DecimalField(
        verbose_name="POC viral load count",
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="",
    )

    time_of_test = models.DateTimeField(
        verbose_name="Test Date and time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    time_of_result = models.DateTimeField(
        verbose_name="Result Date and time",
        validators=[datetime_not_future],
        help_text="Time it takes to obtain viral load result.",
        null=True,
        blank=True,
    )

    easy_of_use = models.CharField(
        verbose_name="Ease of use by field operator?",
        max_length=200,
        choices=EASY_OF_USE,
    )

    stability = EncryptedTextField(
        verbose_name="Stability",
        max_length=250,
        null=True,
        blank=True,
        help_text="Comment")

    history = HistoricalRecords()

    quota = QuotaManager()

    def pre_order(self):
        url = reverse('admin:bcpp_lab_preorder_changelist')
        return '<a href="{0}?q={1}">pre_orders</a>'.format(url, self.subject_visit.subject_identifier)
    pre_order.allow_tags = True

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "POC VL"
        verbose_name_plural = "POC VL"
