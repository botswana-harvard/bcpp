from datetime import date
from dateutil.relativedelta import relativedelta

from django.test import TestCase
from django.test.utils import override_settings

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc.core.bhp_variables.models import StudySite
from edc_map.site_mappers import site_mappers
from edc_constants.constants import NO

from bhp066.apps.bcpp_household.models import HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory, RepresentativeEligibilityFactory
from bhp066.apps.member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.member.choices import ANNUAL, ABSENT, REFUSED
from bhp066.apps.member.models import HouseholdMember
from bhp066.apps.bcpp_survey.models import Survey

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
from bhp066.apps.bcpp_subject.models.call_list import CallList
from bhp066.apps.member.tests.factories import SubjectAbsenteeEntryFactory
from bhp066.apps.member.models import SubjectAbsentee
from bhp066.apps.member.tests.factories import SubjectRefusalFactory

from .factories import SubjectConsentFactory, SubjectVisitFactory
from bhp066.apps.bcpp_subject.tests.factories.subject_locator_factory import SubjectLocatorFactory
from bhp066.apps.member.tests.factories import SubjectAbsenteeFactory
from bhp066.apps.member.models import SubjectAbsenteeEntry

from ..classes import UpdateCallList


class TestUpdateCallList(TestCase):

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-1',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def setUp(self):
        site_mappers.autodiscover()
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        self.app_config = BcppAppConfiguration()
        self.app_config.prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.mapper = site_mappers.get_current_mapper()
#         self.app_config.prep_survey_for_tests()

        self.community = 'test_community'
        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')

        survey = Survey.objects.all().order_by('datetime_start')[0]

        self.study_site = StudySite.objects.get(site_code='01')

        self.household_structure = HouseholdStructure.objects.get(household__plot=plot, survey=survey)
        RepresentativeEligibilityFactory(household_structure=self.household_structure)

        self.male_dob = date.today() - relativedelta(years=25)
        self.male_age_in_years = 25
        self.male_first_name = 'ERIK'
        self.male_initials = "EW"

        self.household_member_male_T0 = HouseholdMemberFactory(
            household_structure=self.household_structure, gender='M',
            age_in_years=self.male_age_in_years, first_name=self.male_first_name,
            initials=self.male_initials
        )

        EnrollmentChecklistFactory(
            household_member=self.household_member_male_T0,
            gender='M',
            citizen='Yes',
            dob=self.male_dob,
            guardian='No',
            initials=self.household_member_male_T0.initials,
            part_time_resident='Yes'
        )

        self.subject_consent_male = SubjectConsentFactory(household_member=self.household_member_male_T0, study_site=self.study_site, gender='M', dob=self.male_dob, first_name=self.male_first_name, initials=self.male_initials)

        self.registered_subject_male = RegisteredSubject.objects.get(subject_identifier=self.subject_consent_male.subject_identifier)

        self.appointment_male_T0 = Appointment.objects.get(registered_subject=self.registered_subject_male, visit_definition__code='T0')

        self.subject_visit_male_T0 = SubjectVisitFactory(appointment=self.appointment_male_T0, household_member=self.household_member_male_T0)
        SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject, subject_visit=self.subject_visit_male_T0)
        self.household_member_T1 = None
        self.update_call_list_class = UpdateCallList()

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-2',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_update_call_list1(self):
        """Test creation of a year 2 household member who is consented and their member status has to be annual."""

        self.update_call_list_class.update_call_list('test_community', 'bcpp-year-1', 't1-prep')
        self.assertEqual(HouseholdMember.objects.filter(
            household_structure__survey__survey_slug='bcpp-year-2').count(), 1)

        household_member = HouseholdMember.objects.get(household_structure__survey__survey_slug='bcpp-year-2', internal_identifier=self.household_member_male_T0.internal_identifier)
        self.assertEqual(household_member.member_status, ANNUAL)
        self.assertEqual(CallList.objects.filter(household_member=household_member).count(), 1)

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-2',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def overiding_settings_file(self):
        self.update_call_list_class.update_call_list('test_community', 'bcpp-year-1', 't1-prep')
        return HouseholdMember.objects.get(household_structure__survey__survey_slug='bcpp-year-2')

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-3',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_update_call_list2(self):
        """Test creation of a year 3 household member who is consented and their member status has to be annual."""

        self.household_member_T1 = self.overiding_settings_file()
        registered_subject = self.household_member_T1.registered_subject

        self.update_call_list_class.update_call_list('test_community', 'bcpp-year-2', 't2-prep')

        self.assertEqual(HouseholdMember.objects.filter(
            household_structure__survey__survey_slug='bcpp-year-3').count(), 1)

        household_member_year3 = HouseholdMember.objects.get(household_structure__survey__survey_slug='bcpp-year-3')

        self.assertEqual(CallList.objects.filter(household_member=household_member_year3).count(), 1)
        self.assertEqual(household_member_year3.member_status, ANNUAL)
        self.assertEqual(CallList.objects.filter(household_member=household_member_year3).count(), 1)
        self.assertEqual(HouseholdMember.objects.filter(registered_subject=registered_subject).count(), 3)

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-2',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_annual_member_absentee(self):
        """Test if the member status of an annual member who is absent is calculated correctly."""
        self.update_call_list_class.update_call_list('test_community', 'bcpp-year-1', 't1-prep')
        self.assertEqual(HouseholdMember.objects.filter(
            household_structure__survey__survey_slug='bcpp-year-2').count(), 1)

        household_member = HouseholdMember.objects.get(household_structure__survey__survey_slug='bcpp-year-2', internal_identifier=self.household_member_male_T0.internal_identifier)
        self.assertEqual(household_member.member_status, ANNUAL)
        self.assertEqual(CallList.objects.filter(household_member=household_member).count(), 1)
        household_member.member_status = ABSENT
        household_member.save()
        absentee = SubjectAbsenteeFactory(household_member=household_member)
        SubjectAbsenteeEntryFactory(subject_absentee=absentee)
        self.assertEquals(SubjectAbsentee.objects.filter(household_member=household_member).count(), 1)
        self.assertEquals(SubjectAbsenteeEntry.objects.filter(subject_absentee=absentee).count(), 1)
        SubjectAbsenteeEntryFactory(subject_absentee=absentee)
        self.assertEquals(SubjectAbsenteeEntry.objects.filter(subject_absentee=absentee).count(), 2)
        SubjectAbsenteeEntryFactory(subject_absentee=absentee)
        self.assertEquals(SubjectAbsenteeEntry.objects.filter(subject_absentee=absentee).count(), 3)
        household_member = HouseholdMember.objects.get(household_structure__survey__survey_slug='bcpp-year-2', internal_identifier=self.household_member_male_T0.internal_identifier)
        self.assertEqual(household_member.member_status, ABSENT)

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-2',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_annual_member_refusal(self):
        """Test if the member status of an annual member who has refused is calculated correctly."""
        self.update_call_list_class.update_call_list('test_community', 'bcpp-year-1', 't1-prep')
        self.assertEqual(HouseholdMember.objects.filter(
            household_structure__survey__survey_slug='bcpp-year-2').count(), 1)

        household_member = HouseholdMember.objects.get(household_structure__survey__survey_slug='bcpp-year-2', internal_identifier=self.household_member_male_T0.internal_identifier)
        self.assertEqual(household_member.member_status, ANNUAL)
        self.assertEqual(CallList.objects.filter(household_member=household_member).count(), 1)

        household_member.member_status = REFUSED
        household_member.save(update_fields=['member_status'])
        self.assertFalse(household_member.refused)

        household_member = HouseholdMember.objects.get(pk=household_member.pk)
        SubjectRefusalFactory(household_member=household_member)
        self.assertEqual(household_member.member_status, REFUSED)
        self.assertTrue(household_member.refused)
#         if self.mapper.intervention:
#             self.assertEqual(household_member.member_status, REFUSED)
#             self.assertTrue(household_member.refused)
#         else:
#             self.assertEqual(household_member.member_status, HTC_ELIGIBLE)
#             self.assertTrue(household_member.refused)
#         self.assertEqual(household_member.member_status, REFUSED)

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-2',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_annual_member_absent(self):
        """Test if the member status of an annual member who is absent is calculated correctly."""
        self.update_call_list_class.update_call_list('test_community', 'bcpp-year-1', 't1-prep')
        self.assertEqual(HouseholdMember.objects.filter(
            household_structure__survey__survey_slug='bcpp-year-2').count(), 1)

        household_member = HouseholdMember.objects.get(household_structure__survey__survey_slug='bcpp-year-2', internal_identifier=self.household_member_male_T0.internal_identifier)
        self.assertEqual(household_member.member_status, ANNUAL)
        self.assertEqual(CallList.objects.filter(household_member=household_member).count(), 1)

        household_member.present_today = NO
        household_member.save(update_fields=['present_today'])

        household_member = HouseholdMember.objects.get(pk=household_member.pk)
        self.assertTrue(household_member.absent)
        self.assertEqual(household_member.member_status, ABSENT)
