import factory

from datetime import date, datetime

from bhp066.apps.bcpp_subject.models import Pregnancy


class PregnancyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Pregnancy

    report_datetime = datetime.today()
    lnmp = date.today()
