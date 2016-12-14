from edc.subject.visit_tracking.tests.factories import BaseVisitTrackingFactory
from bhp066.apps.bcpp_subject.models import SubjectVisit


class SubjectVisitFactory(BaseVisitTrackingFactory):
    FACTORY_FOR = SubjectVisit
