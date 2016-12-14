import factory
from datetime import date, datetime
from bhp066.apps.bcpp_subject.models import SubstanceUse
from edc_constants.constants import YES


class SubstanceUseFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SubstanceUse

    report_datetime = datetime.today()
    alcohol = 'Never'
    smoke = YES
