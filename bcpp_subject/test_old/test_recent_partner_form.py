from django.test import TestCase
from django.utils import timezone
from django.test.utils import override_settings

from dateutil.relativedelta import relativedelta
from datetime import date, datetime

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc.core.bhp_variables.models import StudySite
from edc.subject.appointment.models import Appointment

from edc_constants.choices import YES, NO, NOT_APPLICABLE

from bhp066.apps.bcpp_household.models import HouseholdStructure
from bhp066.apps.member.models import HouseholdMember
from bhp066.apps.bcpp_household.tests.factories import PlotFactory, RepresentativeEligibilityFactory
from bhp066.apps.member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.member.classes import EnumerationHelper

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile

from edc.map.classes.controller import site_mappers
from bhp066.apps.bcpp_subject.tests.factories.subject_consent_factory import SubjectConsentFactory
from bhp066.apps.bcpp_subject.models import SubjectConsent
from bhp066.apps.bcpp_household.models.household_log import HouseholdLog, HouseholdLogEntry
from bhp066.apps.bcpp_household.tests.factories.household_log_entry_factory import HouseholdLogEntryFactory
from bhp066.apps.member.tests.factories.head_household_factory import HeadHouseholdEligibilityFactory
from bhp066.apps.member.tests.factories.household_info_factory import HouseholdInfoFactory
from .factories import (SubjectConsentFactory, SubjectVisitFactory)


class TestMostRecentForm(TestCase):

    app_label = 'bcpp_subject'
    community = 'test_community'

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-2',
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
        self.appointment = Appointment.objects.get(
                    registered_subject=self.household_member_male_T0.registered_subject, visit_definition__code='T0')

        self.subject_visit = SubjectVisitFactory(household_member=self.household_member_male_T0, appointment=self.appointment)

        self.registered_subject = RegisteredSubject.objects.get(subject_identifier=self.subject_consent_male.subject_identifier)

        self.sexual_data = {
            'subject_visit': self.subject_visit.id,
            'alcohol_sex': 'Myself',
            'report_datetime': datetime.today(),
            'condom': NO,
            'more_sex': NO,
            'ever_sex': YES,
            'first_sex': 20,
            'last_year_partners': None,
            'lifetime_sex_partners': 1,
            'more_sex': None,
            'subject_visit_id': None,
            'user_modified': u'',
            }
        self.data = {
            'subject_visit': self.subject_visit.id,
            'concurrent': NO,
            'first_partner_live': None,
            'first_condom_freq': u'Sometimes',
            'first_disclose': u'Yes',
            'first_exchange': u'30-39',
            'first_first_sex': u'Years',
            'first_first_sex_calc': 3L,
            'first_haart': None,
            'first_partner_arm': None,
            'first_partner_cp': u'No',
            'first_partner_hiv': u'not_sure',
            'first_relationship': u'Long-term partner',
            'first_sex_current': u'Yes',
            'first_sex_freq': None,
            'goods_exchange': u'No',
            'partner_hiv_test': u'not_sure',
            'past_year_sex_freq': u'About once a month',
            'report_datetime': datetime.today(),
            'sex_partner_community': u'N/A',
            'subject_visit_id': None,
            'third_last_sex': u'Days',
            'third_last_sex_calc': 7L,
            'user_modified': u''}

    def create_household_log_entry(self, household_structure):
        household_log = HouseholdLog.objects.filter(household_structure=household_structure).last()
        HouseholdLogEntry.objects.all().delete()
        HouseholdLogEntryFactory(household_log=household_log)

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-1',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_subject_recent_form_valid(self):
        """ For all participants who are above 64 at bhs are not eligible."""
        from bhp066.apps.bcpp_subject.forms.months_partner_form import MonthsRecentPartnerForm
        from bhp066.apps.bcpp_subject.forms.sexual_behaviour_form import SexualBehaviourForm
        sexual_behaviour_form = SexualBehaviourForm(data=self.sexual_data)
        sexual_behaviour_form.save()
        self.assertTrue(sexual_behaviour_form.is_valid())
        from bhp066.apps.bcpp_list.models import PartnerResidency
        parnter_residency = PartnerResidency.objects.create(name='In this community.')
        self.data['first_partner_live'] = [parnter_residency.id]
        recent_form = MonthsRecentPartnerForm(data=self.data)

        self.assertTrue(recent_form.is_valid())

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-1',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_subject_recent_form_valid1(self):
        """ For all participants who are above 64 at bhs are not eligible."""
        from bhp066.apps.bcpp_subject.forms.months_partner_form import MonthsRecentPartnerForm
        from bhp066.apps.bcpp_subject.forms.sexual_behaviour_form import SexualBehaviourForm
        sexual_behaviour_form = SexualBehaviourForm(data=self.sexual_data)
        sexual_behaviour_form.save()
        self.assertTrue(sexual_behaviour_form.is_valid())
        from bhp066.apps.bcpp_list.models import PartnerResidency
        parnter_residency = PartnerResidency.objects.create(name='In this community.')
        self.data['first_partner_live'] = [parnter_residency.id]
        self.data['concurrent'] = 'DWTA'
        recent_form = MonthsRecentPartnerForm(data=self.data)

        self.assertTrue(recent_form.is_valid())

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-1',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_subject_recent_form_not_valid(self):
        """ For all participants who are above 64 at bhs are not eligible."""
        from bhp066.apps.bcpp_subject.forms.months_partner_form import MonthsRecentPartnerForm
        from bhp066.apps.bcpp_subject.forms.sexual_behaviour_form import SexualBehaviourForm
        sexual_behaviour_form = SexualBehaviourForm(data=self.sexual_data)
        sexual_behaviour_form.save()
        print sexual_behaviour_form.errors
        self.assertTrue(sexual_behaviour_form.is_valid())
        from bhp066.apps.bcpp_list.models import PartnerResidency
        parnter_residency = PartnerResidency.objects.create(name='In this community.')
        self.data['concurrent'] = YES
        self.data['first_partner_live'] = [parnter_residency.id]
        recent_form = MonthsRecentPartnerForm(data=self.data)
        msg = "Please correct if you have sex with other partners"
        err_msg = u"You wrote that you have only one partner ever in sexual behavior form. {}".format(msg)
        #self.assertIn(u"sex", recent_form.errors.get("__all__"))
        self.assertFalse(recent_form.is_valid())
