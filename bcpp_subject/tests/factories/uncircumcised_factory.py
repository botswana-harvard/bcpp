import factory

from datetime import date, datetime

from bhp066.apps.bcpp_subject.models import Uncircumcised
from edc_constants.constants import YES


class UncircumcisedFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Uncircumcised

    report_datetime = datetime.today()
    future_circ = YES
