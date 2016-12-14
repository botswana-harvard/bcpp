import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import Pima
from edc_constants.constants import YES


class PimaFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Pima

    report_datetime = datetime.today()
    pima_today = YES
    pima_id = factory.Sequence(lambda n: 'pima_id{0}'.format(n))
    cd4_value = 2.5
