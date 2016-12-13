from django.test import TestCase
from django.test.utils import override_settings

from dateutil.relativedelta import relativedelta
from datetime import date, datetime

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc.core.bhp_variables.models import StudySite

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


class TestSubjectConsentForm(TestCase):

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
        self.data = {
            'last_name': 'WIZZY', 'is_minor': 'No',
            'witness_name': None, 'is_literate': 'Yes', 'subject_type': 'subject',
            'consent_copy': 'Yes', 'is_verified': False, 'consent_signature': None, 'first_name': 'ERIK',
            'dm_comment': None,
            'is_dob_estimated': None, 'verified_by': None, 'user_modified': u'', 'is_signed': True,
            'subject_identifier_aka': None, 'version': u'4',
            'citizen': 'Yes', 'legal_marriage': u'N/A', 'assessment_score': 'Yes',
            'is_incarcerated': 'No', 'consent_reviewed': 'Yes', 'study_questions': 'Yes',
            'study_site_id': self.study_site.id,
            'may_store_samples': YES,
            'community': u'test_community', 'using': 'default', 'marriage_certificate_no': None,
            'identity': '317918515',
            'confirm_identity': '317918515',
            'identity_type': 'OMANG',
            'language': u'not specified',
            'guardian_name': None, 'gender': 'M',
            'household_member': self.household_member_male_T0.id,
            'marriage_certificate': u'N/A', 'dob': self.male_dob,
            'study_site': self.study_site.id,
            'initials': 'EW',
            'language': 'en',
            'is_dob_estimated': '-',
            'consent_signature': YES,
            'consent_datetime': datetime.today(),
            'version': 1
        }

    def create_household_log_entry(self, household_structure):
        household_log = HouseholdLog.objects.filter(household_structure=household_structure).last()
        HouseholdLogEntry.objects.all().delete()
        HouseholdLogEntryFactory(household_log=household_log)

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-2',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_subject_consent_age_above_64_at_bhs(self):
        """ For all participants who are above 64 at bhs are not eligible."""
        from bhp066.apps.bcpp_subject.forms.subject_consent_form import SubjectConsentForm
        self.male_dob = date.today() - relativedelta(years=65)
        self.data['dob'] = self.male_dob
        self.data['household_member'] = self.household_member_male_T0.id
        consent_form = SubjectConsentForm(data=self.data)
        self.assertIn(
            u"Subject's age is 65y. Subject is not eligible for consent.", consent_form.errors.get("__all__"))

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-1',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_subject_consent_age_within_65_at_bhs(self):
        """ For all participants within 65 at bhs are eligible."""
        self.app_config.prep_survey_for_tests()
        self.subject_consent_male.version = 2
        self.subject_consent_male.save_base()
        from bhp066.apps.bcpp_subject.forms.subject_consent_form import SubjectConsentForm
        dob = date.today() - relativedelta(years=64)
        self.household_member_male_T0.age_in_years = 64
        self.household_member_male_T0.save()
        self.enrollment.dob = dob
        self.enrollment.save_base()
        self.data['dob'] = dob
        self.data['identity'] = '317918514'
        self.data['confirm_identity'] = '317918514'
        consent_form = SubjectConsentForm(data=self.data)
        print consent_form.errors
        consent_form.save()
        self.assertEqual(RegisteredSubject.objects.filter(identity=self.data['identity']).count(), 1)

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-2',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_subject_consent_age_above_64_at_ahs(self):
        """ Test identity on
        """

        dob = date.today() - relativedelta(years=65)
        self.household_member_male_T0.age_in_years = 65
        self.household_member_male_T0.save_base()
        self.subject_consent_male.dob = dob
        self.enrollment.dob = dob
        self.enrollment.save_base()
        self.subject_consent_male.save_base()

        self.app_config.prep_survey_for_tests()
        from bhp066.apps.bcpp_subject.forms.subject_consent_form import SubjectConsentForm

        enumeration_helper = EnumerationHelper(self.household_structure_ahs.household, self.survey_bhs, self.survey_ahs)
        enumeration_helper.add_members_from_survey()
        self.household_member = HouseholdMember.objects.get(
            registered_subject__identity='101119811',
            household_structure__survey=self.survey_ahs,
        )
        dob = date.today() - relativedelta(years=65)
        self.household_member.age_in_years = 65
        self.household_member.save_base()

        HeadHouseholdEligibilityFactory(
            household_member=self.household_member, household_structure=self.household_member.household_structure)
        self.enrollment.dob = dob
        self.enrollment.save_base()

        self.subject_consent = SubjectConsent.objects.get(household_member=self.household_member_male_T0)
        self.subject_consent.version = 2
        self.subject_consent.save_base()

        self.create_household_log_entry(self.household_structure_ahs)

        self.data['dob'] = dob
        self.data['household_member'] = self.household_member.id
        self.data['identity'] = '101119811'
        self.data['confirm_identity'] = '101119811'
        consent_form = SubjectConsentForm(data=self.data)
        print consent_form.errors
        self.assertTrue(consent_form.is_valid())

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-2',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_subject_consent_age_within_65_at_ahs(self):
        """ Test identity on
        """
        self.app_config.prep_survey_for_tests()
        from bhp066.apps.bcpp_subject.forms.subject_consent_form import SubjectConsentForm

        enumeration_helper = EnumerationHelper(self.household_structure_ahs.household, self.survey_bhs, self.survey_ahs)
        enumeration_helper.add_members_from_survey()
        self.household_member = HouseholdMember.objects.get(
            registered_subject__identity='101119811',
            household_structure__survey=self.survey_ahs
        )
        HeadHouseholdEligibilityFactory(
            household_member=self.household_member, household_structure=self.household_member.household_structure)
        self.subject_consent = SubjectConsent.objects.get(household_member=self.household_member_male_T0)
        self.subject_consent.version = 2
        self.subject_consent.save_base()

        self.data['household_member'] = self.household_member.id
        self.data['identity'] = '101119811'
        self.data['confirm_identity'] = '101119811'

        self.create_household_log_entry(self.household_structure_ahs)

        consent_form = SubjectConsentForm(data=self.data)
        self.assertTrue(consent_form.is_valid())

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-2',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_surname_marrige_at_ahs(self):
        """ Test identity on
        """
        self.app_config.prep_survey_for_tests()
        from bhp066.apps.bcpp_subject.forms.subject_consent_form import SubjectConsentForm
        enumeration_helper = EnumerationHelper(self.household_structure_ahs.household, self.survey_bhs, self.survey_ahs)
        enumeration_helper.add_members_from_survey()
        self.household_member = HouseholdMember.objects.get(
            registered_subject__identity='101119811',
            household_structure__survey=self.survey_ahs
        )
        self.household_member.personal_details_changed = YES
        self.household_member.details_change_reason = 'married'
        self.household_member.last_name = 'SETSIBA'
        self.household_member.initials = 'ES'
        self.household_member.save()

        self.create_household_log_entry(self.household_structure_ahs)

        HeadHouseholdEligibilityFactory(
            household_member=self.household_member, household_structure=self.household_member.household_structure)

        self.subject_consent = SubjectConsent.objects.get(household_member=self.household_member_male_T0)
        self.subject_consent.version = 2
        self.subject_consent.save_base()
        self.data['household_member'] = self.household_member.id
        self.data['identity'] = '101119811'
        self.data['confirm_identity'] = '101119811'
        self.data['last_name'] = 'SETSIBA'
        self.data['initials'] = 'ES'
        consent_form = SubjectConsentForm(data=self.data)
        self.assertTrue(consent_form.is_valid())
        consent_form.save()
        consent = SubjectConsent.objects.get(household_member=self.household_member)
        consent_form = SubjectConsentForm(data=self.data, instance=consent)
        consent_form.save()

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-1',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_validate_legal_marriage_at_bhs(self):
        self.data['citizen'] = NO
        self.data['identity'] = '101119811'
        self.data['confirm_identity'] = '101119811'
        from bhp066.apps.bcpp_subject.forms.subject_consent_form import SubjectConsentForm
        self.data['legal_marriage'] = YES
        self.data['marriage_certificate'] = YES
        self.data['marriage_certificate_no'] = '12421'
        self.enrollment.citizen = NO
        self.enrollment.save_base()
        consent_form = SubjectConsentForm(data=self.data)
        print consent_form.errors
        self.assertTrue(consent_form.is_valid())

    @override_settings(
        SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-1',
        CURRENT_COMMUNITY_CHECK=False,
        LIMIT_EDIT_TO_CURRENT_SURVEY=True,
        LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
        FILTERED_DEFAULT_SEARCH=True,
    )
    def test_validate_legal_marriage_at_bhs_not_valid(self):
        self.data['citizen'] = NO
        self.data['identity'] = '101119811'
        self.data['confirm_identity'] = '101119811'
        from bhp066.apps.bcpp_subject.forms.subject_consent_form import SubjectConsentForm
        self.data['legal_marriage'] = YES
        self.data['marriage_certificate'] = YES
        self.enrollment.citizen = NO
        self.enrollment.save_base()
        consent_form = SubjectConsentForm(data=self.data)
        self.assertIn(u'You wrote subject is NOT a citizen and has marriage certificate. Please provide certificate number.', consent_form.errors.get("__all__"))
        self.assertFalse(consent_form.is_valid())
