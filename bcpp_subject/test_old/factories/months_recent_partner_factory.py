import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import MonthsRecentPartner
from edc_constants.constants import YES


class MonthsRecentPartnerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MonthsRecentPartner

    report_datetime = datetime.today()
    third_last_sex = 'Days'
    third_last_sex_calc = 2
    first_first_sex = 'Days'
    first_first_sex_calc = 2
    first_sex_current = YES
    first_relationship = 'Long-term partner'
    concurrent = YES
    goods_exchange = YES
    first_sex_freq = 2
    partner_hiv_test = YES
