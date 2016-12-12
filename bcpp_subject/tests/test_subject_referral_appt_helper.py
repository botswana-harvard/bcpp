from datetime import datetime, date
from dateutil.relativedelta import MO, TU, WE, TH, FR
from datetime import timedelta

from django.test import TestCase


from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_household.utils.clinic_days_tuple import ClinicDaysTuple
from edc.map.classes.controller import site_mappers

CLINIC_DAYS = {
    '96': {'IDCC': ClinicDaysTuple((MO, ), None),
           'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), date(2014, 11, 24))},
    '97': {'IDCC': ClinicDaysTuple((MO, ), None),
           'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), date(2014, 11, 24))},
    '98': {'IDCC': ClinicDaysTuple((MO, WE), None),
           'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'SMC': ClinicDaysTuple((MO, TU, WE, TH, FR), date(2014, 11, 24))},
    '99': {'IDCC': ClinicDaysTuple((MO, WE), None),
           'ANC': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'VCT': ClinicDaysTuple((MO, TU, WE, TH, FR), None),
           'SMC': ClinicDaysTuple((WE, ), date(2014, 11, 15))},
    }


class TestSubjectReferralApptHelper(TestCase):
    """Tests given a referral code correctly calculates the next appointment datetime.

    The calculated appointment dates will differ according to the referral code"""

    def test_masa1(self):
        """Assert give a clinic day in two weeks for a MASA client at the IDCC with no appointment"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        expected_appt_day = 'Mon'
        today = date(2014, 8, 25)
        expected_appt_datetime = datetime(2014, 9, 8, 7, 30, 0)
        hiv_care_adherence_next_appointment = datetime(2014, 9, 8, 7, 30, 0)
        community_code = '97'
        referral_code = 'MASA-CC'
        scheduled_appt_date = None
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            scheduled_appt_date=scheduled_appt_date,
            community_code=community_code,
            community_clinic_days=CLINIC_DAYS.get(community_code),
            hiv_care_adherence_next_appointment=hiv_care_adherence_next_appointment)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa1a(self):
        """Assert give a clinic day in two weeks for a MASA client at the IDCC with no appointment"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        expected_appt_day = 'Mon'
        today = date(2014, 8, 25)
        expected_appt_datetime = datetime(2014, 9, 8, 7, 30, 0)
        hiv_care_adherence_next_appointment = datetime(2014, 9, 8, 7, 30, 0)
        community_code = '98'
        referral_code = 'MASA-CC'
        scheduled_appt_date = None
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            scheduled_appt_date=scheduled_appt_date,
            community_code=community_code,
            community_clinic_days=CLINIC_DAYS.get(community_code),
            hiv_care_adherence_next_appointment=hiv_care_adherence_next_appointment)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa1b(self):
        """Assert give a clinic day in two weeks for a MASA client at the IDCC with no appointment"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        expected_appt_day = 'Mon'
        today = date(2014, 8, 25)
        expected_appt_datetime = datetime(2014, 9, 8, 7, 30, 0)
        hiv_care_adherence_next_appointment = datetime(2014, 9, 8, 7, 30, 0)
        community_code = '96'
        referral_code = 'MASA-CC'
        scheduled_appt_date = None
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            scheduled_appt_date=scheduled_appt_date,
            community_code=community_code,
            community_clinic_days=CLINIC_DAYS.get(community_code),
            hiv_care_adherence_next_appointment=hiv_care_adherence_next_appointment)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa1c(self):
        """Assert give a clinic day in two weeks for a MASA client at the IDCC with no appointment"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today_day = 'Th'
        expected_appt_day = 'Mon'
        today = date(2015, 2, 13)
        expected_appt_datetime = datetime(2015, 2, 23, 7, 30, 0)
        hiv_care_adherence_next_appointment = datetime(2015, 2, 23, 7, 30, 0)
        community_code = '97'
        referral_code = 'MASA-CC'
        scheduled_appt_date = None#date(2015, 2, 25)
        #next_appointment_date = date(2015, 3, 4)
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            scheduled_appt_date=scheduled_appt_date,
            community_code=community_code,
            community_clinic_days=CLINIC_DAYS.get(community_code),
            hiv_care_adherence_next_appointment=hiv_care_adherence_next_appointment)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa2(self):
        """Assert give next clinic day MASA client at the IDCC that is a suspected defaulter with no appointment"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        expected_appt_day = 'Wed'
        today = date(2014, 8, 25)
        expected_appt_datetime = datetime(2014, 8, 27, 7, 30, 0)
        community_code = '98'
        referral_code = 'MASA-DF'
        scheduled_appt_date = None
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            scheduled_appt_date=scheduled_appt_date,
            community_code=community_code,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa2a(self):
        """Assert give next clinic day MASA client at the IDCC that is a suspected defaulter with an appointment"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        expected_appt_day = 'Wed'
        today = date(2014, 8, 25)
        scheduled_appt_date = date(2014, 9, 17)
        expected_appt_datetime = datetime(2014, 8, 27, 7, 30, 0)
        community_code = '98'
        referral_code = 'MASA-DF'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a referral datetime of {0}. Got {1}'.format(expected_appt_datetime, referral_appt_datetime))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa3(self):
        """Assert give next clinic day in 3 weels for a MASA client at the IDCC with a scheduled appt in 3 weeks"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today_day = 'Tue'
        expected_appt_day = 'Wed'
        today = date(2014, 8, 26)
        scheduled_appt_date = date(2014, 9, 17)
        expected_appt_datetime = datetime(2014, 9, 17, 7, 30, 0)
        hiv_care_adherence_next_appointment =  datetime(2014, 9, 17, 7, 30, 0)
        community_code = '98'
        referral_code = 'MASA-CC'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code),
            hiv_care_adherence_next_appointment=hiv_care_adherence_next_appointment)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa4(self):
        """Assert give next clinic day in two weeks for a MASA client at the IDCC with a scheduled appt in 2 weeks"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today_day = 'Tue'
        expected_appt_day = 'Mon'
        today = date(2014, 8, 26)
        scheduled_appt_date = datetime(2014, 9, 9, 7, 30, 0)
        expected_appt_datetime = datetime(2014, 9, 15, 7, 30, 0)
        hiv_care_adherence_next_appointment = datetime(2014, 9, 15, 7, 30, 0)
        community_code = '98'
        referral_code = 'MASA-CC'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code),
            hiv_care_adherence_next_appointment=hiv_care_adherence_next_appointment)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_masa5(self):
        """Assert give two week appointment if scheduled appt is more than a month away."""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today_day = 'Tue'
        expected_appt_day = 'Mon'
        today = date(2014, 8, 26)
        scheduled_appt_date = datetime(2014, 9, 29, 7, 30, 0)
        expected_appt_datetime = datetime(2014, 9, 29, 7, 30, 0)
        community_code = '98'
        referral_code = 'MASA-CC'
        hiv_care_adherence_next_appointment = datetime(2014, 9, 29, 7, 30, 0)
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code),
            hiv_care_adherence_next_appointment=hiv_care_adherence_next_appointment)
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_smc1(self):
        """Assert referred on smc_start date for SMC subjected seen on a date before the smc start date"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today = datetime.today().date()
        today_day = self.next_workday(today).strftime("%A")[:3]
        expected_appt_day = self.next_workday(today).strftime("%A")[:3]
        scheduled_appt_date = None
        expected_appt_datetime = datetime((datetime.today() + timedelta(days=1)).year, (datetime.today() + timedelta(days=1)).month, (datetime.today() + timedelta(days=1)).day,  7, 30, 0)
        expected_appt_datetime = self.next_workday(expected_appt_datetime)
        community_code = '98'
        referral_code = 'SMC-NEG'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(subject_referral_appt_helper.referral_clinic_type, 'SMC')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_smc1a(self):
        """Assert referred on ECC smc_start date for SMC subjected seen on a date before the smc start date (start date is SAT)"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today = datetime.today().date()
        today_day = self.next_workday(today).strftime("%A")[:3]
        expected_appt_day = self.next_workday(today).strftime("%A")[:3]
        scheduled_appt_date = None
        expected_appt_datetime = datetime((datetime.today() + timedelta(days=1)).year, (datetime.today() + timedelta(days=1)).month, (datetime.today() + timedelta(days=1)).day,  7, 30, 0)
        expected_appt_datetime = self.next_workday(expected_appt_datetime)
        community_code = '99'
        referral_code = 'SMC-NEG'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(subject_referral_appt_helper.referral_clinic_type, 'SMC')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_smc1b(self):
        """Assert referred on CPC smc_start date for SMC subjected seen on a date over the weekend (start date is SAT)"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today = datetime.today().date()
        today_day = self.next_workday(today).strftime("%A")[:3]
        expected_appt_day = self.next_workday(today).strftime("%A")[:3]
        scheduled_appt_date = None
        expected_appt_datetime = datetime((datetime.today() + timedelta(days=1)).year, (datetime.today() + timedelta(days=1)).month, (datetime.today() + timedelta(days=1)).day, 7, 30, 0)
        expected_appt_datetime = self.next_workday(expected_appt_datetime)
        community_code = '99'
        referral_code = 'SMC-NEG'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(subject_referral_appt_helper.referral_clinic_type, 'SMC')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_smc1c(self):
        """Assert referred on ECC smc_start date for SMC subjected seen on a date over the weekend (start date is SAT)"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today = date.today()
        scheduled_appt_date = None
        expected_appt_datetime = None
        community_code = '99'
        referral_code = 'SMC-NEG'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        self.assertEqual(subject_referral_appt_helper.referral_clinic_type, 'SMC')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime)

    def test_smc2(self):
        """Assert referred on on smc day for SMC subjected seen on a date AFTER the smc start date (TU->WE)"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today = datetime.today().date()
        today_day = self.next_workday(today).strftime("%A")[:3]
        expected_appt_day = self.next_workday(today).strftime("%A")[:3]
        scheduled_appt_date = None
        expected_appt_datetime = datetime((datetime.today() + timedelta(days=1)).year, (datetime.today() + timedelta(days=1)).month, (datetime.today() + timedelta(days=1)).day,  7, 30, 0)
        expected_appt_datetime = self.next_workday(expected_appt_datetime)
        community_code = '98'
        referral_code = 'SMC-NEG'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        self.assertEqual(subject_referral_appt_helper.referral_clinic_type, 'SMC')
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        print "referral_appt_day", referral_appt_day
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_smc3(self):
        """Assert referred on on smc day for SMC subjected seen on a date AFTER the smc start date (SA->MO)"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today = datetime.today().date()
        today_day = self.next_workday(today).strftime("%A")[:3]
        expected_appt_day = self.next_workday(today).strftime("%A")[:3]
        scheduled_appt_date = None
        expected_appt_datetime = datetime((datetime.today() + timedelta(days=1)).year, (datetime.today() + timedelta(days=1)).month, (datetime.today() + timedelta(days=1)).day,  7, 30, 0)
        expected_appt_datetime = self.next_workday(expected_appt_datetime)
        community_code = '98'
        referral_code = 'SMC-NEG'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(subject_referral_appt_helper.referral_clinic_type, 'SMC')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_hiv1(self):
        """Assert referred to VCT testing"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today_day = 'Sat'
        expected_appt_day = 'Mon'
        today = date(2014, 11, 1)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 11, 3, 7, 30, 0)
        community_code = '98'
        referral_code = 'TST-HIV'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_hiv2(self):
        """Assert referred POS#-HI to IDCC testing"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today_day = 'Sat'
        expected_appt_day = 'Mon'
        today = date(2014, 11, 1)
        expected_appt_datetime = datetime(2014, 11, 3, 7, 30, 0)
        community_code = '98'
        referral_code = 'POS#-HI'
        scheduled_appt_date = None
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_hiv3(self):
        """Assert referred POS#-HI to IDCC testing"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today_day = 'Sat'
        expected_appt_day = 'Mon'
        today = date(2014, 11, 1)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 11, 3, 7, 30, 0)
        community_code = '98'
        referral_code = 'POS#-LO'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_hiv4(self):
        """Assert referred POS#-HI to IDCC testing"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today_day = 'Sat'
        expected_appt_day = 'Mon'
        today = date(2014, 11, 1)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 11, 3, 7, 30, 0)
        community_code = '98'
        referral_code = 'POS!-LO'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_hiv5(self):
        """Assert referred POS#-HI to IDCC testing"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        today_day = 'Sat'
        expected_appt_day = 'Mon'
        today = date(2014, 11, 1)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2014, 11, 3, 7, 30, 0)
        community_code = '98'
        referral_code = 'POS!-HI'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))

    def test_POS_next_clinic_day(self):
        """Test that POS! will get the next clinic date"""
        from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper
        expected_appt_day = 'Wed'
        today = date(2015, 3, 2)
        scheduled_appt_date = None
        expected_appt_datetime = datetime(2015, 3, 4, 7, 30, 0)
        community_code = '98'
        referral_code = 'POS!-HI'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))
        # Test with only 1 IDCC day.
        expected_appt_day = 'Mon'
        expected_appt_datetime = datetime(2015, 3, 9, 7, 30, 0)
        community_code = '96'
        referral_code = 'POS!-HI'
        subject_referral_appt_helper = SubjectReferralApptHelper(
            referral_code,
            base_date=today,
            community_code=community_code,
            scheduled_appt_date=scheduled_appt_date,
            community_clinic_days=CLINIC_DAYS.get(community_code))
        referral_appt_datetime = subject_referral_appt_helper.referral_appt_datetime
        referral_appt_day = referral_appt_datetime.strftime('%a')
        self.assertEqual(referral_appt_datetime, expected_appt_datetime, 'Expected a {4} referral datetime of {0}{1}. '
                         'Got {2}{3}'.format(expected_appt_day, expected_appt_datetime,
                                             referral_appt_day, referral_appt_datetime, subject_referral_appt_helper.referral_clinic_type))
        self.assertEqual(referral_appt_day,
                         expected_appt_day,
                         'Expected {0} {1} from next_clinic_date(). Got {2} {3}'.format(
                             expected_appt_day,
                             expected_appt_datetime,
                             referral_appt_day,
                             referral_appt_datetime))
    def next_workday(self, today):
        """This method returns the next week day that is not a holyday and is not a weekend."""
        holidays = []
        next_workday = datetime((today + timedelta(days=1)).year, (datetime.today() + timedelta(days=1)).month, (datetime.today() + timedelta(days=1)).day, 7, 30, 0)
        for _, holyday_date in BcppAppConfiguration.holidays_setup.iteritems():
            holidays.append(holyday_date)
        if next_workday.date() not in holidays:
            if next_workday.isoweekday() == 6:
                next_workday = datetime(( next_workday + timedelta(days=1)).year, (datetime.today() + timedelta(days=1)).month, (datetime.today() + timedelta(days=3)).day, 7, 30, 0)
            elif next_workday.isoweekday() == 7 and next_workday.date() not in holidays:
                next_workday = datetime((next_workday + timedelta(days=1)).year, (datetime.today() + timedelta(days=1)).month, (datetime.today() + timedelta(days=1)).day, 7, 30, 0)
        else:
            next_workday = datetime((datetime.today() + timedelta(days=1)).year, (datetime.today() + timedelta(days=1)).month, (datetime.today() + timedelta(days=1)).day, 7, 30, 0)
            next_workday()
        return next_workday
