import factory
from datetime import date, datetime
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from edc_constants.constants import YES

from bhp066.apps.bcpp_subject.models import CeaEnrollmentChecklist


class CeaEnrollmentChecklistFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CeaEnrollmentChecklist

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    citizen = YES
    community_resident = YES
    enrollment_reason = 'CD4 < 50'
    cd4_date = date.today()
    cd4_count = 2.5
    opportunistic_illness = 'Tuberculosis'
    diagnosis_date = date.today()
    date_signed = datetime.today()
