import factory

from datetime import date, datetime

from bhp066.apps.bcpp_subject.models import Sti


class StiFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Sti

    report_datetime = datetime.today()
    sti_date = date.today()
    sti_dx = 'wasting'
