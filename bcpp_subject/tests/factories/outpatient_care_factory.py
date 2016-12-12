import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import OutpatientCare
from edc_constants.constants import YES


class OutpatientCareFactory(factory.DjangoModelFactory):
    FACTORY_FOR = OutpatientCare

    report_datetime = datetime.today()
    govt_health_care = YES
    dept_care = YES
    prvt_care = YES
    trad_care = YES
    facility_visited = 'Government Clinic/Post'
    care_reason = 'HIV-related care'
    care_reason_other = factory.Sequence(lambda n: 'care_reason_other{0}'.format(n))
    outpatient_expense = 2.5
    travel_time = 'Under 0.5 hour'
    transport_expense = 2.5
    cost_cover = YES
    waiting_hours = 'Under 0.5 hour'
