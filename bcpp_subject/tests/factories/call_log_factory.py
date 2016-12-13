import factory

from bhp066.apps.member.tests.factories import HouseholdMemberFactory
from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory

from bhp066.apps.bcpp_subject.models import CallLog


class CallLogFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CallLog

    household_member = factory.SubFactory(HouseholdMemberFactory)
    survey = factory.SubFactory(SurveyFactory)
    label = factory.Sequence(lambda n: 'label{0}'.format(n))
    locator_information = factory.Sequence(lambda n: 'locator_information{0}'.format(n))
