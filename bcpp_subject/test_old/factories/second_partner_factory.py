import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import MonthsSecondPartner
from edc_constants.constants import MALE, YES, POS


class SecondPartnerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MonthsSecondPartner

    report_datetime = datetime.today()
    rel_type = 'Longterm partner'
    rel_type_other = factory.Sequence(lambda n: 'rel_type_other{0}'.format(n))
    partner_residency = 'In this community'
    partner_age = 2
    partner_gender = MALE
    last_sex_contact = 2
    last_sex_contact_other = factory.Sequence(lambda n: 'last_sex_contact_other{0}'.format(n))
    first_sex_contact = 2
    first_sex_contact_other = factory.Sequence(lambda n: 'first_sex_contact_other{0}'.format(n))
    regular_sex = 2
    having_sex_reg = 'All of the time'
    alcohol_before_sex = YES
    partner_status = POS
