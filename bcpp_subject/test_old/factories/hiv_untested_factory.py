import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import HivUntested


class HivUntestedFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivUntested

    report_datetime = datetime.today()
