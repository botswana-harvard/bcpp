import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import NonPregnancy
from edc_constants.constants import YES


class NonPregnancyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = NonPregnancy

    report_datetime = datetime.today()
    more_children = YES
