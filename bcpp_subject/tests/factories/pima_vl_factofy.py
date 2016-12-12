import factory

from datetime import datetime

from edc_constants.constants import YES

from bhp066.apps.bcpp_subject.models import PimaVl

from .base_scheduled_model_factory import BaseScheduledModelFactory


class PimaVlFactory(BaseScheduledModelFactory):
    FACTORY_FOR = PimaVl
    report_datetime = datetime.today()
    poc_vl_today = YES
    poc_vl_type = 'mobile setting'
    poc_vl_datetime = datetime.today()
    time_of_test = datetime.today()
    time_of_result = datetime.today()
    easy_of_use = 'easy'
    pima_id = factory.Sequence(lambda n: 'pima_id{0}'.format(n))
    poc_vl_value = 1000
