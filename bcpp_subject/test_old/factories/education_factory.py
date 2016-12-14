import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import Education
from edc_constants.constants import YES


class EducationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Education

    report_datetime = datetime.today()
    education = 'None'
    working = YES
