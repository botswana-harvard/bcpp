import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import ResourceUtilization
from edc_constants.constants import YES


class ResourceUtilizationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ResourceUtilization

    report_datetime = datetime.today()
    out_patient = YES
    money_spent = 2.5
    medical_cover = YES
