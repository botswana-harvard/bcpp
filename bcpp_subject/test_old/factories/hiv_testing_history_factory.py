import factory

from datetime import datetime

from .subject_visit_factory import SubjectVisitFactory

from bhp066.apps.bcpp_subject.models import HivTestingHistory
from edc_constants.constants import YES, NEG, NO


class HivTestingHistoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivTestingHistory

    subject_visit = factory.SubFactory(SubjectVisitFactory)
    report_datetime = datetime.today()
    has_tested = YES
    has_record = YES
    verbal_hiv_result = NEG
    other_record = NO
