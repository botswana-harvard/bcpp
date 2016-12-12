import factory
from datetime import date, datetime

from bhp066.apps.bcpp_subject.models import HivResult

from .base_scheduled_model_factory import BaseScheduledModelFactory
from edc_constants.constants import POS


class HivResultFactory(BaseScheduledModelFactory):
    FACTORY_FOR = HivResult

    report_datetime = datetime.today()
    hiv_result = POS
