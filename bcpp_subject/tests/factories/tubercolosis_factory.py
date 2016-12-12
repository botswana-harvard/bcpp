import factory
from datetime import date, datetime
from bhp066.apps.bcpp_subject.models import Tubercolosis


class TubercolosisFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Tubercolosis

    report_datetime = datetime.today()
    date_tb = date.today()
    dx_tb = 'Pulmonary tuberculosis'
