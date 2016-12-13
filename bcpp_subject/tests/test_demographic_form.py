from django.test import TestCase
from django.utils import timezone
from django.test.utils import override_settings

from dateutil.relativedelta import relativedelta
from datetime import date, datetime

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.core.bhp_variables.models import StudySite
from edc.subject.appointment.models.appointment import Appointment

from bhp066.apps.bcpp_household.models import HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory, RepresentativeEligibilityFactory
from bhp066.apps.member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_survey.models import Survey

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile

from edc.map.classes.controller import site_mappers
from bhp066.apps.bcpp_subject.tests.factories.subject_consent_factory import SubjectConsentFactory
from bhp066.apps.bcpp_household.models.household_log import HouseholdLog, HouseholdLogEntry
from bhp066.apps.bcpp_household.tests.factories.household_log_entry_factory import HouseholdLogEntryFactory
from bhp066.apps.member.tests.factories.head_household_factory import HeadHouseholdEligibilityFactory
from bhp066.apps.member.tests.factories.household_info_factory import HouseholdInfoFactory
from bhp066.apps.bcpp_subject.tests.factories._subject_visit_factory import SubjectVisitFactory
from bhp066.apps.bcpp_list.models.religion import Religion
from bhp066.apps.bcpp_list.models.live_with import LiveWith
from bhp066.apps.bcpp_list.models.ethnic_groups import EthnicGroups
from bhp066.apps.member.classes.enumeration_helper import EnumerationHelper
from bhp066.apps.member.models.household_member import HouseholdMember


class TestSubjectConsentForm(TestCase):

    app_label = 'bcpp_subject'
    community = 'test_community'

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-1',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def setUp(self):
        site_mappers.autodiscover()
        from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        self.app_config = BcppAppConfiguration()
        self.app_config.prepare()
        self.app_config.prep_survey_for_tests()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()

        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')

        self.survey_bhs = Survey.objects.get(survey_slug='bcpp-year-1')

        self.survey_ahs = Survey.objects.get(survey_slug='bcpp-year-2')

        self.study_site = StudySite.objects.get(site_code='01')

        self.household_structure_bhs = HouseholdStructure.objects.get(household__plot=plot, survey=self.survey_bhs)
        self.household_structure_ahs = HouseholdStructure.objects.get(household__plot=plot, survey=self.survey_ahs)
        self.create_household_log_entry(self.household_structure_bhs)

        RepresentativeEligibilityFactory(household_structure=self.household_structure_bhs)

        self.male_dob = date.today() - relativedelta(years=25)
        self.male_age_in_years = 25
        self.male_first_name = 'ERIK'
        self.male_last_name = 'HIEWAI'
        self.male_initials = "EW"

        self.household_member_male_T0 = HouseholdMemberFactory(
            household_structure=self.household_structure_bhs, gender='M',
            age_in_years=self.male_age_in_years, first_name=self.male_first_name,
            initials=self.male_initials
        )

        HeadHouseholdEligibilityFactory(
            household_member=self.household_member_male_T0, household_structure=self.household_structure_bhs)
        self.household_member_male_T0.eligible_hoh = True
        self.household_member_male_T0.save()

        HouseholdInfoFactory(
            household_member=self.household_member_male_T0, household_structure=self.household_structure_bhs,
            registered_subject=self.household_member_male_T0.registered_subject
        )

        self.enrollment = EnrollmentChecklistFactory(
            household_member=self.household_member_male_T0,
            gender='M',
            citizen='Yes',
            dob=self.male_dob,
            guardian='No',
            initials=self.household_member_male_T0.initials,
            part_time_resident='Yes'
        )

        self.subject_consent_male = SubjectConsentFactory(
            household_member=self.household_member_male_T0, confirm_identity='101119811', identity='101119811',
            study_site=self.study_site, gender='M', dob=self.male_dob, first_name=self.male_first_name,
            initials=self.male_initials)

        appointment_male = Appointment.objects.get(
            registered_subject=self.household_member_male_T0.registered_subject, visit_definition__code='T0')

        subject_visit_male = SubjectVisitFactory(
            appointment=appointment_male, household_member=self.household_member_male_T0)

        ethic_data = {
            'display_index': 0L,
            'field_name': None,
            'id': 1L,
            'name': u'Babirwa',
        }
        religion_data = {
            'display_index': 0L,
            'field_name': None,
            'name': u'Anglican',
            'revision': None,
            'short_name': u'anglican',
        }
        live_with_data = {
            'id': 1L,
            'name': u'Partner or spouse',
            'revision': None,
            'short_name': u'Partner or spouse',
        }
        ethic = EthnicGroups.objects.create(**ethic_data)
        live_with = LiveWith.objects.create(**live_with_data)
        religion = Religion.objects.create(**religion_data)
        self.data = {
            'ethnic_other': '',
            'husband_wives': None,
            'marital_status': 'Married',
            'modified': datetime.today(),
            'num_wives': 2,
            'live_with': [live_with.id],
            'religion': [religion.id],
            'religion_other': u'',
            'report_datetime': datetime.today(),
            'subject_visit': subject_visit_male.id,
            'ethnic': [ethic.id]
        }

    def create_household_log_entry(self, household_structure):
        household_log = HouseholdLog.objects.filter(household_structure=household_structure).last()
        HouseholdLogEntry.objects.all().delete()
        HouseholdLogEntryFactory(household_log=household_log)

    def test_marriage_gender_female_valid(self):
        """ Test identity on
        """
        self.data['num_wives'] = None
        self.data['husband_wives'] = 10
        from bhp066.apps.bcpp_subject.forms import DemographicsForm
        demo_form = DemographicsForm(data=self.data)
        self.assertTrue(demo_form.is_valid())

    def test_marriage_gender_female_not_valid(self):
        """ Test identity on
        """
        self.data['num_wives'] = 10
        self.data['husband_wives'] = None
        from bhp066.apps.bcpp_subject.forms import DemographicsForm
        demo_form = DemographicsForm(data=self.data)
        self.assertFalse(demo_form.is_valid())
        self.assertIn(
            u"You should fill the number of wives.", demo_form.errors.get("__all__"))

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-2',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_marriage_gender_female_annual_valid(self):
        """ Test identity on
        """
        enumeration_helper_T2 = EnumerationHelper(self.household_structure_bhs.household, self.survey_bhs, self.survey_ahs)
        enumeration_helper_T2.add_members_from_survey()
        self.data['num_wives'] = None
        self.data['husband_wives'] = 10
        self.household_member_male = HouseholdMember.objects.get(household_structure=self.household_structure_ahs)
        self.subject_consent_male.version = 2
        self.subject_consent_male.save_base()
        self.subject_consent_male = SubjectConsentFactory(
            household_member=self.household_member_male, confirm_identity='101119811', identity='101119811',
            study_site=self.study_site, gender='M', dob=self.male_dob, first_name=self.male_first_name,
            initials=self.male_initials, version=4)

        appointment_male = Appointment.objects.get(
            registered_subject=self.household_member_male_T0.registered_subject, visit_definition__code='T1')

        subject_visit_male = SubjectVisitFactory(
            appointment=appointment_male, household_member=self.household_member_male)
        self.data['subject_visit'] = subject_visit_male.id
        from bhp066.apps.bcpp_subject.forms import DemographicsForm
        demo_form = DemographicsForm(data=self.data)
        self.assertTrue(demo_form.is_valid())
#         self.assertIn(
#             u"You should fill the number of wives.", demo_form.errors.get("__all__"))

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-2',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_marriage_gender_female_annual_notvalid(self):
        """ Test identity on
        """
        enumeration_helper_T2 = EnumerationHelper(self.household_structure_bhs.household, self.survey_bhs, self.survey_ahs)
        enumeration_helper_T2.add_members_from_survey()
        self.data['num_wives'] = 10
        self.data['husband_wives'] = None
        self.household_member_male = HouseholdMember.objects.get(household_structure=self.household_structure_ahs)
        self.subject_consent_male.version = 2
        self.subject_consent_male.save_base()
        self.subject_consent_male = SubjectConsentFactory(
            household_member=self.household_member_male, confirm_identity='101119811', identity='101119811',
            study_site=self.study_site, gender='M', dob=self.male_dob, first_name=self.male_first_name,
            initials=self.male_initials, version=4)

        appointment_male = Appointment.objects.get(
            registered_subject=self.household_member_male_T0.registered_subject, visit_definition__code='T1')

        subject_visit_male = SubjectVisitFactory(
            appointment=appointment_male, household_member=self.household_member_male)
        self.data['subject_visit'] = subject_visit_male.id
        from bhp066.apps.bcpp_subject.forms import DemographicsForm
        demo_form = DemographicsForm(data=self.data)
        self.assertFalse(demo_form.is_valid())
        self.assertIn(
            u"You should fill the number of wives.", demo_form.errors.get("__all__"))
