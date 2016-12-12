from datetime import datetime

from bhp066.apps.bcpp_subject.models import Circumcision

from ..factories import BaseScheduledModelFactory
from edc_constants.constants import YES


class CircumcisionFactory(BaseScheduledModelFactory):
    FACTORY_FOR = Circumcision

    report_datetime = datetime.today()
    circumcised = YES
