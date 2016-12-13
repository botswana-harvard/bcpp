import factory
from datetime import datetime

from edc.core.bhp_variables.tests.factories import StudySiteFactory

from bhp066.apps.bcpp_subject.tests.factories import SubjectVisitFactory

from ..factories import PanelFactory
from ..factories import AliquotTypeFactory
from ...models import SubjectRequisition


class SubjectRequisitionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SubjectRequisition

    subject_visit = factory.SubFactory(SubjectVisitFactory)
    aliquot_type = factory.SubFactory(AliquotTypeFactory)
    panel = factory.SubFactory(PanelFactory)
    site = factory.SubFactory(StudySiteFactory)
    requisition_datetime = datetime.today()
    drawn_datetime = datetime.today()
    is_drawn = 'Yes'
