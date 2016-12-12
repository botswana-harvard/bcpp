import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import SexualBehaviour
from edc_constants.constants import YES


class SexualBehaviourFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SexualBehaviour

    report_datetime = datetime.today()
    ever_sex = YES
