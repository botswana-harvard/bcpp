import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import Stigma


class StigmaFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Stigma

    report_datetime = datetime.today()
    anticipate_stigma = 'Strongly disagree'
    enacted_shame_stigma = 'Strongly disagree'
    saliva_stigma = 'Strongly disagree'
    teacher_stigma = 'Strongly disagree'
    children_stigma = 'Strongly disagree'
