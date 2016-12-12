from datetime import datetime, date
from dateutil.relativedelta import MO, TU, WE, TH, FR

from django.test import SimpleTestCase

from bhp066.apps.bcpp_household.utils import ClinicDaysTuple

from ..utils import next_clinic_date


CLINIC_DAYS = {
    '11': {'IDCC': ClinicDaysTuple((MO, WE), None),
           'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), date(2016, 05, 17)),
           'SMC-ECC': ClinicDaysTuple((MO, TU, WE, TH, FR), date(2016, 05, 17))},
    '12': {'IDCC': ClinicDaysTuple((MO, WE), None),
           'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), date(2016, 05, 17)),
           'SMC-ECC': ClinicDaysTuple((MO, TU, WE, TH, FR), date(2016, 05, 17))},
}


class TestNextClinicDate(SimpleTestCase):
    """Test that given today's date next_clinic_date() selects the
    next appointment day from a tuple of days for a given CLINIC
    and suggests a date that is not today."""
    today_day = None
    expected_appt_day = None
    today = None
    expected_appt_datetime = None
    community_code = None
    clinic = None
    community_clinic_days = None
    referral_code = None

    def calc_date(self):
        self.community_clinic_days = CLINIC_DAYS.get(self.community_code)
        print self.community_clinic_days
        self.assertEqual(self.today.strftime('%a'), self.today_day, 'Today is not a {0}'.format(self.today_day))
        self.assertEqual(self.expected_appt_datetime.strftime('%a'),
                         self.expected_appt_day,
                         'Expected clinic day is not a {0}'.format(self.expected_appt_day))
        calculated_appt_datetime = next_clinic_date(self.community_clinic_days.get(self.clinic),
                                                    base_datetime=self.today)
        calculated_appt_day = calculated_appt_datetime.strftime('%a')
        self.assertEqual(calculated_appt_day,
                         self.expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             self.expected_appt_day,
                             self.expected_appt_datetime,
                             calculated_appt_day,
                             calculated_appt_datetime))
        self.assertEqual(next_clinic_date(self.community_clinic_days.get(self.clinic),
                                          base_datetime=self.today,
                                          ),
                         self.expected_appt_datetime)

    def test_idcc1(self):
        """Assert give Mon get Tue"""
        self.today_day = 'Mon'
        self.expected_appt_day = 'Wed'
        self.today = date(2016, 05, 16)
        self.expected_appt_datetime = datetime(2016, 05, 18, 7, 30, 0)
        self.community_code = '11'
        self.clinic = 'IDCC'
        self.calc_date()

    def test_idcc2(self):
        """Assert give Tue get Wed"""
        self.today_day = 'Tue'
        self.expected_appt_day = 'Wed'
        self.today = date(2014, 8, 19)
        self.expected_appt_datetime = datetime(2014, 8, 20, 7, 30, 0)
        self.community_code = '11'
        self.clinic = 'IDCC'
        self.calc_date()

    def test_idcc3(self):
        """Assert give Wed get next Mon"""
        self.today_day = 'Wed'
        self.expected_appt_day = 'Mon'
        self.today = date(2014, 8, 20)
        self.expected_appt_datetime = datetime(2014, 8, 25, 7, 30, 0)
        self.community_code = '11'
        self.clinic = 'IDCC'
        self.calc_date()

    def test_idcc4(self):
        """Assert give Sat get next Mon"""
        self.today_day = 'Sat'
        self.expected_appt_day = 'Mon'
        self.today = date(2014, 8, 23)
        self.expected_appt_datetime = datetime(2014, 8, 25, 7, 30, 0)
        self.community_code = '11'
        self.clinic = 'IDCC'
        self.calc_date()

    def test_idcc5(self):
        """Assert give Sun get next Mon"""
        self.today_day = 'Sun'
        self.expected_appt_day = 'Mon'
        self.today = date(2014, 8, 24)
        self.expected_appt_datetime = datetime(2014, 8, 25, 7, 30, 0)
        self.community_code = '11'
        self.clinic = 'IDCC'
        self.calc_date()

    def test_smc5(self):
        """Assert give Sat get next Mon"""
        self.today_day = 'Sun'
        self.expected_appt_day = 'Mon'
        self.today = date(2014, 8, 24)
        self.expected_appt_datetime = datetime(2014, 8, 25, 7, 30, 0)
        self.community_code = '11'
        self.clinic = 'SMC'
        self.calc_date()

    def test_smc6(self):
        """Assert give Sat get next Mon"""
        self.today_day = 'Mon'
        self.expected_appt_day = 'Tue'
        self.today = date(2014, 8, 25)
        self.expected_appt_datetime = datetime(2014, 8, 26, 7, 30, 0)
        self.community_code = '11'
        self.clinic = 'SMC'
        self.calc_date()

    def test_same_day(self):
        """Assert give Sat get next Mon"""
        community_clinic_days = CLINIC_DAYS.get('11')
        self.today_day = 'Mon'
        self.expected_appt_day = 'Tue'
        self.today = date(2014, 8, 25)
        self.expected_appt_datetime = datetime(2014, 8, 25, 7, 30, 0)
        self.community_code = '11'
        self.clinic = 'IDCC'
        self.assertEqual(next_clinic_date(community_clinic_days.get(self.clinic),
                                          base_datetime=self.today,
                                          allow_same_day=True),
                         self.expected_appt_datetime)

    def test_previous_day(self):
        """Assert that next clinic day can get revious day from a date"""
        community_clinic_days = CLINIC_DAYS.get('11')
        self.today_day = 'Mon'
        self.expected_appt_day = 'Wed'
        self.today = date(2014, 9, 25)
        self.expected_appt_datetime = datetime(2014, 9, 24, 7, 30, 0)
        self.clinic = 'IDCC'
        self.assertEqual(next_clinic_date(community_clinic_days.get(self.clinic),
                                          base_datetime=self.today,
                                          allow_same_day=True,
                                          subtract=True),
                         self.expected_appt_datetime)

    def test_previous_day2(self):
        """Assert that next clinic day can get revious day from a date"""
        community_clinic_days = CLINIC_DAYS.get('11')
        self.today_day = 'Mon'
        self.expected_appt_day = 'Wed'
        self.today = date(2014, 9, 24)
        self.expected_appt_datetime = datetime(2014, 9, 22, 7, 30, 0)
        self.clinic = 'IDCC'
        self.assertEqual(next_clinic_date(community_clinic_days.get(self.clinic),
                                          base_datetime=self.today,
                                          allow_same_day=False,
                                          subtract=True),
                         self.expected_appt_datetime)
