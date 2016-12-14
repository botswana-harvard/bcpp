import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import PositiveParticipant


class PositiveParticipantFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PositiveParticipant

    report_datetime = datetime.today()
    internalize_stigma = 'Strongly'
    internalized_stigma = 'Strongly disagree'
    friend_stigma = 'Strongly disagree'
    family_stigma = 'Strongly disagree'
    enacted_talk_stigma = 'Strongly disagree'
    enacted_respect_stigma = 'Strongly disagree'
    enacted_jobs_tigma = 'Strongly disagree'
