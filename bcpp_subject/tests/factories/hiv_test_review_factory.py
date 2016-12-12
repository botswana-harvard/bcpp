import factory

from datetime import date, datetime

from bhp066.apps.bcpp_subject.models import HivTestReview
from edc_constants.constants import POS


class HivTestReviewFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivTestReview

    report_datetime = datetime.today()
    hiv_test_date = date.today()
    recorded_hiv_result = POS
