from datetime import date
from django.test import TestCase
from django.conf import settings
from dateutil.relativedelta import relativedelta

from edc_constants.constants import YES, NO

# from ..classes import ValidateCallListHouseholdMember
from .factories import SubjectConsentFactory
from ..models import SubjectConsent

from edc.core.bhp_variables.models import StudySite
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from edc_map.site_mappers import site_mappers

from bhp066.apps.bcpp_household.models import HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory, RepresentativeEligibilityFactory
from bhp066.apps.member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_survey.models import Survey


class TestValidateCallListHouseholdMember(TestCase):

    def setUp(self):
        site_mappers.autodiscover()
        from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
        try:
            site_lab_profiles.register(BcppSubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()
        site_mappers.autodiscover()
        self.community = settings.CURRENT_COMMUNITY
        self.site_code = site_mappers.get_mapper(self.community)

        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')

        surveys = Survey.objects.all().order_by('datetime_start')
        survey_T0 = surveys[0]
        survey_T1 = surveys[1]
        survey_T2 = surveys[2]

        self.study_site = StudySite.objects.get(site_code='01')

        self.household_structure = HouseholdStructure.objects.get(household__plot=plot, survey=survey_T0)
        self.household_structure_y2 = HouseholdStructure.objects.get(household__plot=plot, survey=survey_T1)
        self.household_structure_y3 = HouseholdStructure.objects.get(household__plot=plot, survey=survey_T2)
        RepresentativeEligibilityFactory(household_structure=self.household_structure)
        RepresentativeEligibilityFactory(household_structure=self.household_structure_y2)
        RepresentativeEligibilityFactory(household_structure=self.household_structure_y3)
        HouseholdMemberFactory(household_structure=self.household_structure)
        HouseholdMemberFactory(household_structure=self.household_structure)
        HouseholdMemberFactory(household_structure=self.household_structure)

        male_dob = date.today() - relativedelta(years=25)
        male_age_in_years = 25
        male_first_name = 'ERIK'
        male_initials = "EW"
        female_dob = date.today() - relativedelta(years=35)
        female_age_in_years = 35
        female_first_name = 'ERIKA'
        female_initials = "EW"

        self.household_member_female_T0 = HouseholdMemberFactory(household_structure=self.household_structure, gender='F', age_in_years=female_age_in_years, first_name=female_first_name, initials=female_initials)
        self.household_member_male_T0 = HouseholdMemberFactory(household_structure=self.household_structure, gender='M', age_in_years=male_age_in_years, first_name=male_first_name, initials=male_initials)
        self.household_member_female_T0.member_status = 'BHS_SCREEN'
        self.household_member_male_T0.member_status = 'BHS_SCREEN'
        self.household_member_female_T0.save()
        self.household_member_male_T0.save()
        EnrollmentChecklistFactory(
            household_member=self.household_member_female_T0,
            gender='F',
            citizen=YES,
            dob=female_dob,
            guardian=NO,
            initials=self.household_member_female_T0.initials,
            part_time_resident=YES)
        EnrollmentChecklistFactory(
            household_member=self.household_member_male_T0,
            gender='M',
            citizen=YES,
            dob=male_dob,
            guardian=NO,
            initials=self.household_member_male_T0.initials,
            part_time_resident=YES)
        SubjectConsentFactory(household_member=self.household_member_female_T0, confirm_identity='101129811', identity='101129811', study_site=self.study_site, gender='F', dob=female_dob, first_name=female_first_name, initials=female_initials)
        SubjectConsentFactory(household_member=self.household_member_male_T0, confirm_identity='101119811', identity='101119811', study_site=self.study_site, gender='M', dob=male_dob, first_name=male_first_name, initials=male_initials)

    def tests_consents(self):
        """Test missing members for the next survey created by call list."""
#         validate_call_list = ValidateCallListHouseholdMember
#         created_consents = 0
#         while created_consents < 5:
#         SubjectConsentFactory()
#             created_consents += 1
        consents = SubjectConsent.objects.all()
        self.assertEqual(consents.count(), 2)
