import factory

from datetime import datetime

from .labour_market_wages_factory import LabourMarketWagesFactory

from bhp066.apps.bcpp_subject.models import Grant


class GrantFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Grant

    report_datetime = datetime.today()
    labour_market_wages = factory.SubFactory(LabourMarketWagesFactory)
    grant_number = 2
    grant_type = 'Child support '
    other_grant = factory.Sequence(lambda n: 'other_grant{0}'.format(n))
