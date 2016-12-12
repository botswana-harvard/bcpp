import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import HivHealthCareCosts
from edc_constants.constants import YES


class HivHealthCareCostsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivHealthCareCosts

    report_datetime = datetime.today()
    hiv_medical_care = YES
    place_care_received = 'Government dispensary'
    care_regularity = '0 times'
    doctor_visits = 'always'
