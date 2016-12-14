import factory

from datetime import date, datetime

from edc.subject.registration.tests.factories import RegisteredSubjectFactory

from .subject_visit_factory import SubjectVisitFactory

from bhp066.apps.bcpp_subject.models import SubjectLocator
from edc_constants.constants import YES


class SubjectLocatorFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SubjectLocator

    subject_visit = factory.SubFactory(SubjectVisitFactory)
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    report_datetime = datetime.today()
    date_signed = date.today()
    home_visit_permission = YES
    subject_cell = '72777777'
    may_follow_up = YES
    may_call_work = YES
    may_contact_someone = YES
    has_alt_contact = YES
