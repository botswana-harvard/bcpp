import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import Cd4History


class Cd4HistoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Cd4History

    report_datetime = datetime.today()
