import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import TbSymptoms
from edc_constants.constants import YES, NO


class TbSymptomsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = TbSymptoms

    report_datetime = datetime.today()
    cough = YES
    cough_blood = YES
    night_sweat = YES
    weight_loss = NO
    fever = NO
