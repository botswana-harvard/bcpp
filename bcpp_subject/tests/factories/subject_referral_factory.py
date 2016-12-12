import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import SubjectReferral


class SubjectReferralFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SubjectReferral

    report_datetime = datetime.today()
