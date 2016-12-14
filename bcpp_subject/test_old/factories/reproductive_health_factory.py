import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import ReproductiveHealth
from edc_constants.constants import YES


class ReproductiveHealthFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ReproductiveHealth

    report_datetime = datetime.today()
    number_children = 2
    menopause = YES
    family_planning_other = factory.Sequence(lambda n: 'family_planning_other{0}'.format(n))
