import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import StigmaOpinion


class StigmaOpinionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = StigmaOpinion

    report_datetime = datetime.today()
    test_community_stigma = 'Strongly disagree'
    gossip_community_stigma = 'Strongly disagree'
    respect_community_stigma = 'Strongly disagree'
    enacted_verbal_stigma = 'Strongly disagree'
    enacted_phyical_stigma = 'Strongly disagree'
    enacted_family_stigma = 'Strongly disagree'
    fear_stigma = 'Strongly disagree'
