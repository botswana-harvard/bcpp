import factory
from datetime import datetime

from django.conf import settings

from bhp066.apps.member.tests.factories import HouseholdMemberFactory

from bhp066.apps.bcpp_subject.models import CallList


class CallListFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CallList

    household_member = factory.SubFactory(HouseholdMemberFactory)
    community = settings.CURRENT_COMMUNITY
    subject_identifier = factory.Sequence(lambda n: '066-21444678-{0}'.format(n))
    first_name = factory.Sequence(lambda n: 'ONIZA{0}'.format(n))
    initials = factory.Sequence(lambda n: 'OP{0}'.format(n))
    gender = 'F'
    consent_datetime = datetime.today()
    call_attempts = 1
    call_status = 'Open'
