import factory

from datetime import datetime

from .subject_consent_factory import SubjectConsentFactory

from bhp066.apps.bcpp_subject.models import CorrectConsent


class CorrectConsentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CorrectConsent

    subject_consent = factory.SubFactory(SubjectConsentFactory)
    report_datetime = datetime.today()
