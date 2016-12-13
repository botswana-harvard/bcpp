import factory
from datetime import datetime, date
from edc.testing.tests.factories.test_consent_factory import BaseConsentFactory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from bhp066.apps.bcpp_subject.models import SubjectConsent
from bhp066.apps.member.tests.factories import HouseholdMemberFactory
from edc_constants.constants import MALE, YES


class SubjectConsentFactory(BaseConsentFactory):

    class Meta:
        model = SubjectConsent

    household_member = factory.SubFactory(HouseholdMemberFactory)
    gender = MALE
    dob = date(1980, 01, 01)
    initials = 'XX'
    subject_identifier = None
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    consent_datetime = datetime.today()
    may_store_samples = YES
    is_literate = YES
    citizen = YES
    is_verified = False
    identity = factory.Sequence(lambda n: 'identity{0}'.format(n))
    confirm_identity = identity
    identity_type = (('OMANG', 'Omang'), ('DRIVERS', "Driver's License"), ('PASSPORT', 'Passport'), ('OMANG_RCPT', 'Omang Receipt'), ('OTHER', 'Other'))[0][0]
    is_signed = True
