from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from django.db.models import get_model
from django.test import TestCase

from edc_map.site_mappers import site_mappers
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.registration.models import RegisteredSubject
from edc.core.bhp_variables.models import StudySite
from edc_constants.constants import NOT_APPLICABLE
from edc.subject.registration.tests.factories import RegisteredSubjectFactory

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_household.models import Household, HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory
from bhp066.apps.bcpp_subject.tests.factories.subject_locator_factory import SubjectLocatorFactory
from bhp066.apps.member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory, SubjectVisitFactory
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory


class BaseScheduledModelTestCase(TestCase):

    app_label = 'bcpp_subject'
    community = 'test_community'
    site_code = None
    study_site = None
    household_strucure = None
    subject_visit_female = None
    subject_visit_male = None

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
        BcppAppConfiguration().prep_survey_for_tests()

        self.household_structure = None
        self.registered_subject = None
        self.representative_eligibility = None
        self.study_site = None
        self.intervention = None

        self.community = site_mappers.get_mapper(site_mappers.current_community).map_area
        self.study_site = StudySite.objects.get(site_code=site_mappers.get_mapper(site_mappers.current_community).map_code)
        self.site_code = self.study_site
        self.intervention = site_mappers.get_mapper(site_mappers.current_community).intervention
        self.survey1 = Survey.objects.get(survey_name='BCPP Year 1')  # see app_configuration
        self.survey2 = Survey.objects.get(survey_name='BCPP Year 2')  # see app_configuration
        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')
        household = Household.objects.get(plot=plot)
        self.create_baseline(household)
        self.create_annual(household)

    def create_baseline(self, household):
        household_structure = HouseholdStructure.objects.get(household=household, survey=self.survey1)
        self.household_structure = household_structure
        RepresentativeEligibilityFactory(household_structure=household_structure)
#         HouseholdMemberFactory(household_structure=household_structure)
#         HouseholdMemberFactory(household_structure=household_structure)
#         HouseholdMemberFactory(household_structure=household_structure)

        HouseholdMember = get_model('member', 'HouseholdMember')

        self.household_member_female = HouseholdMember.objects.create(household_structure=household_structure,
                                                              first_name='SUE', initials='SW', gender='F',
                                                              age_in_years=25, study_resident='Yes', relation='sister',
                                                              inability_to_participate=NOT_APPLICABLE)
        self.household_member_male = HouseholdMember.objects.create(household_structure=household_structure,
                                                            first_name='ERIK', initials='EW', gender='M',
                                                            age_in_years=25, study_resident='Yes', relation='brother',
                                                            inability_to_participate=NOT_APPLICABLE)
#         self.household_member_female.save()
#         self.household_member_male.save()

        enrollment_male = EnrollmentChecklistFactory(
            household_member=self.household_member_male,
            initials=self.household_member_male.initials,
            gender=self.household_member_male.gender,
            dob=date.today() - relativedelta(years=self.household_member_male.age_in_years),
            guardian=NOT_APPLICABLE,
            part_time_resident='Yes',
            citizen='Yes')
        self.household_member_female = HouseholdMember.objects.get(pk=self.household_member_female.pk)

        enrollment_female = EnrollmentChecklistFactory(
            household_member=self.household_member_female,
            initials=self.household_member_female.initials,
            gender=self.household_member_female.gender,
            dob=date.today() - relativedelta(years=self.household_member_female.age_in_years),
            guardian=NOT_APPLICABLE,
            part_time_resident='Yes',
            citizen='Yes')
        self.household_member_male = HouseholdMember.objects.get(pk=self.household_member_male.pk)

        self.subject_consent_female = SubjectConsentFactory(
            consent_datetime=datetime.today(),
            household_member=self.household_member_female,
            registered_subject=self.household_member_female.registered_subject,
            gender='F',
            dob=enrollment_female.dob,
            first_name='SUE',
            last_name='W',
            citizen='Yes',
            confirm_identity='101129811',
            identity='101129811',
            initials=enrollment_female.initials,
            study_site=self.study_site)
        self.subject_consent_male = SubjectConsentFactory(
            consent_datetime=datetime.today(),
            household_member=self.household_member_male,
            registered_subject=self.household_member_male.registered_subject,
            gender='M',
            dob=enrollment_male.dob,
            first_name=self.household_member_male.first_name,
            last_name='W',
            citizen='Yes',
            confirm_identity='101119811',
            identity='101119811',
            initials=enrollment_male.initials,
            study_site=self.study_site)

        self.registered_subject_female = RegisteredSubject.objects.get(subject_identifier=self.subject_consent_female.subject_identifier)
        self.registered_subject_male = RegisteredSubject.objects.get(subject_identifier=self.subject_consent_male.subject_identifier)
        self.appointment_female = Appointment.objects.get(registered_subject=self.registered_subject_female, visit_definition__time_point=0)
        self.subject_visit_female = SubjectVisitFactory(
            report_datetime=datetime.today(),
            appointment=self.appointment_female, household_member=self.household_member_female)
        self.appointment_male = Appointment.objects.get(registered_subject=self.registered_subject_male, visit_definition__time_point=0)
        self.subject_visit_male = SubjectVisitFactory(
            report_datetime=datetime.today(),
            appointment=self.appointment_male, household_member=self.household_member_male)

#     def create_annual(self, household):
        self.household_structure1 = HouseholdStructure.objects.get(household=self.household, survey=self.survey2)
        RepresentativeEligibilityFactory(household_structure=self.household_structure1)

        HouseholdStructure.objects.add_household_members_from_survey(self.household, self.survey1, self.survey2)

        HouseholdMember = get_model('member', 'HouseholdMember')
        self.household_member_female_annual = HouseholdMember.objects.get(
            internal_identifier=self.household_member_female.internal_identifier,
            registered_subject=self.household_member_female.registered_subject,
            household_structure=household_structure)
        self.household_member_male_annual = HouseholdMember.objects.get(
            internal_identifier=self.household_member_male.internal_identifier,
            registered_subject=self.household_member_male.registered_subject,
            household_structure=household_structure)

        self.registered_subject_female_annual = self.household_member_female_annual.registered_subject
        self.registered_subject_male_annual = self.household_member_male_annual.registered_subject
        appointment_female_annual = Appointment.objects.get(registered_subject=self.registered_subject_female, visit_definition__time_point=1)
        self.subject_visit_female_annual = SubjectVisitFactory(
            report_datetime=datetime.today(),
            appointment=appointment_female_annual,
            household_member=self.household_member_female_annual)
        appointment_male_annual = Appointment.objects.get(registered_subject=self.registered_subject_male_annual, visit_definition__time_point=1)
        self.subject_visit_male_annual = SubjectVisitFactory(
            report_datetime=datetime.today(),
            appointment=appointment_male_annual,
            household_member=self.household_member_male_annual)
        SubjectLocatorFactory(subject_visit=self.subject_visit_male)
        SubjectLocatorFactory(subject_visit=self.subject_visit_female)
