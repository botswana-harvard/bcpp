import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import QualityOfLife


class QualityOfLifeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = QualityOfLife

    report_datetime = datetime.today()
    mobility = 'no problems'
    self_care = 'no problems'
    activities = 'no problems'
    pain = 'no pain'
    anxiety = 'not anxious'
