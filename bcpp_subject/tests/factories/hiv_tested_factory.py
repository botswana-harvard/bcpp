import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import HivTested


class HivTestedFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivTested

    report_datetime = datetime.today()
    where_hiv_test = 'Tebelopele VCT center'
    where_hiv_test_other = factory.Sequence(lambda n: 'where_hiv_test_other{0}'.format(n))
