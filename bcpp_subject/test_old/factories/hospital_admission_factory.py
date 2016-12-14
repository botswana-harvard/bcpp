import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import HospitalAdmission
from edc_constants.constants import YES


class HospitalAdmissionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HospitalAdmission

    report_datetime = datetime.today()
    reason_hospitalized = 'HIV-related care'
    facility_hospitalized = factory.Sequence(lambda n: 'facility_hospitalized{0}'.format(n))
    nights_hospitalized = 2
    healthcare_expense = 2.5
    travel_hours = 'Under 0.5 hour'
    hospitalization_costs = YES
