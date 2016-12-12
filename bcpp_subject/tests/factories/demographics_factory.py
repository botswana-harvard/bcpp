import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import Demographics


class DemographicsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Demographics

    report_datetime = datetime.today()
    religion_other = factory.Sequence(lambda n: 'religion_other{0}'.format(n))
    other = factory.Sequence(lambda n: 'other{0}'.format(n))
    marital_status = 'Single/never married'
