import factory
from datetime import datetime
from bhp066.apps.bcpp_subject.models import CommunityEngagement
from edc_constants.constants import YES


class CommunityEngagementFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CommunityEngagement

    report_datetime = datetime.today()
    community_engagement = 'Very active'
    vote_engagement = YES
    problems_engagement_other = factory.Sequence(lambda n: 'problems_engagement_other{0}'.format(n))
    solve_engagement = YES
