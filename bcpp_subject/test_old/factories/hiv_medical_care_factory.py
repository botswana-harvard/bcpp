import factory

from datetime import date, datetime

from bhp066.apps.bcpp_subject.models import HivMedicalCare


class HivMedicalCareFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivMedicalCare

    report_datetime = datetime.today()
    first_hiv_care_pos = date.today()
    last_hiv_care_pos = date.today()
    lowest_cd4 = '0-49'
