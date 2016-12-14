import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import LabourMarketWages

from .subject_visit_factory import SubjectVisitFactory
from edc_constants.constants import YES


class LabourMarketWagesFactory(factory.DjangoModelFactory):
    FACTORY_FOR = LabourMarketWages
    subject_visit = factory.SubFactory(SubjectVisitFactory)
    report_datetime = datetime.today()
    employed = 'government sector'
    occupation_other = factory.Sequence(lambda n: 'occupation_other{0}'.format(n))
    household_income = 'None'
    other_occupation = 'Studying'
    other_occupation_other = factory.Sequence(lambda n: 'other_occupation_other{0}'.format(n))
    govt_grant = YES
    weeks_out = YES
