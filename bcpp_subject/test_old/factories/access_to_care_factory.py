import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import AccessToCare


class AccessToCareFactory(factory.DjangoModelFactory):
    FACTORY_FOR = AccessToCare

    report_datetime = datetime.today()
