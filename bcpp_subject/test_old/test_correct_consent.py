from datetime import date
from dateutil.relativedelta import relativedelta

from django.test import TestCase

from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.appointment.models import Appointment
from edc.subject.rule_groups.classes import site_rule_groups
from edc.core.bhp_variables.models import StudySite
from edc.subject.registration.models import RegisteredSubject
from edc_map.site_mappers import site_mappers

from edc_constants.constants import NEG

from bhp066.apps.member.classes import EnumerationHelper
from bhp066.apps.bcpp_household.tests.factories import PlotFactory
from bhp066.apps.bcpp_subject.tests.factories import (HicEnrollmentFactory, ResidencyMobilityFactory,
                                                      SubjectLocatorFactory, HivResultFactory)
from bhp066.apps.bcpp_subject.models import HicEnrollment
from bhp066.apps.member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory, CorrectConsentFactory, SubjectVisitFactory
from bhp066.apps.member.models import HouseholdMember, EnrollmentChecklist
from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_survey.models import Survey
from bhp066.apps.bcpp_lab.tests.factories import SubjectRequisitionFactory
from bhp066.apps.bcpp_lab.models import Panel, AliquotType
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_household.models import HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory

from ..models import SubjectConsent


class TestCorrectConsent(TestCase):

    app_label = 'bcpp_subject'

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
        self.study_site = StudySite.objects.get(site_code='01')
        self.community = 'test_community'
        self.survey = Survey.objects.all()[0]
        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')
        survey = Survey.objects.all().order_by('datetime_start')[0]
        next_survey = Survey.objects.all().order_by('datetime_start')[1]

        self.household_structure = HouseholdStructure.objects.get(household__plot=plot, survey=survey)
        self.household_structure_y2 = HouseholdStructure.objects.get(household__plot=plot, survey=next_survey)
        RepresentativeEligibilityFactory(household_structure=self.household_structure)
        RepresentativeEligibilityFactory(household_structure=self.household_structure_y2)

        self.female_dob = date(1989, 10, 10)
        self.female_age_in_years = relativedelta(date.today(), self.female_dob).years
        self.female_first_name = 'ERIKA'
        self.female_last_name = 'WAXON'
        self.female_initials = "EW"

        self.household_member_female_T0 = HouseholdMemberFactory(
            household_structure=self.household_structure, gender='F', age_in_years=self.female_age_in_years,
            first_name=self.female_first_name, initials=self.female_initials)
        self.household_member_female_T0.member_status = 'BHS_SCREEN'
        self.household_member_female_T0.save()
        self.assertEqual(self.household_member_female_T0.member_status, 'BHS_SCREEN')
        self.enrollment_checklist_female = EnrollmentChecklistFactory(
            household_member=self.household_member_female_T0,
            gender='F',
            citizen='Yes',
            dob=self.female_dob,
            guardian='No',
            initials=self.household_member_female_T0.initials,
            part_time_resident='Yes')
        self.subject_consent_female = SubjectConsentFactory(
            household_member=self.household_member_female_T0,
            study_site=self.study_site, gender='F', dob=self.female_dob, first_name=self.female_first_name,
            last_name=self.female_last_name, initials=self.female_initials)
        self.registered_subject_female = RegisteredSubject.objects.get(
            subject_identifier=self.subject_consent_female.subject_identifier)

        enumeration_helper = EnumerationHelper(self.household_structure.household, survey, next_survey)
        self.household_member_female = enumeration_helper.create_member_on_target(self.household_member_female_T0)
        self.appointment_female = Appointment.objects.get(registered_subject=self.registered_subject_female, visit_definition__code='T1')
        self.appointment_female_T0 = Appointment.objects.get(registered_subject=self.registered_subject_female, visit_definition__code='T0')
        self.subject_visit_female_T0 = SubjectVisitFactory(appointment=self.appointment_female_T0, household_member=self.household_member_female_T0)
        self.subject_visit_female = SubjectVisitFactory(appointment=self.appointment_female, household_member=self.household_member_female)
        self.locator_female_T0 = SubjectLocatorFactory(subject_visit=self.subject_visit_female_T0, registered_subject=self.registered_subject_female)
        self.residency_mobility_female_T0 = ResidencyMobilityFactory(subject_visit=self.subject_visit_female_T0)
        microtube_panel = Panel.objects.get(name='Microtube')
        aliquot_type = AliquotType.objects.all()[0]
        self.subject_requisition_T0 = SubjectRequisitionFactory(
            subject_visit=self.subject_visit_female_T0,
            panel=microtube_panel,
            aliquot_type=aliquot_type)
        self.hiv_result_today_T0 = HivResultFactory(subject_visit=self.subject_visit_female_T0, hiv_result=NEG)

    def test_lastname_and_initials(self):
        correct_consent = CorrectConsentFactory(
            subject_consent=self.subject_consent_female,
            old_last_name=self.female_last_name,
            new_last_name='DIMSTAR',
        )
        subject_consent = SubjectConsent.objects.get(id=self.subject_consent_female.id)
        self.assertEquals(subject_consent.initials, 'ED')
        self.assertEquals(EnrollmentChecklist.objects.get(id=self.enrollment_checklist_female.id).initials, 'ED')
        self.assertEquals(subject_consent.initials, 'ED')
        self.assertEquals(subject_consent.last_name, 'DIMSTAR')
        self.assertFalse(subject_consent.is_verified)
        self.assertIsNone(subject_consent.is_verified_datetime)
        self.assertIsNone(subject_consent.verified_by)
        if not correct_consent.id:
            self.assertEquals(subject_consent.user_modified, correct_consent.user_created)

    def test_firstname_and_initials(self):
        correct_consent = CorrectConsentFactory(
            subject_consent=self.subject_consent_female,
            old_first_name=self.female_first_name,
            new_first_name='GAME',
        )
        subject_consent = SubjectConsent.objects.get(id=self.subject_consent_female.id)
        self.assertEquals(HouseholdMember.objects.get(id=self.household_member_female_T0.id).initials, 'GW')
        self.assertEquals(EnrollmentChecklist.objects.get(id=self.enrollment_checklist_female.id).initials, 'GW')
        self.assertEquals(HouseholdMember.objects.get(id=self.household_member_female_T0.id).first_name, 'GAME')
        self.assertEquals(subject_consent.first_name, 'GAME')
        self.assertFalse(subject_consent.is_verified)
        self.assertIsNone(subject_consent.is_verified_datetime)
        self.assertIsNone(subject_consent.verified_by)
        if not correct_consent.id:
            self.assertEquals(subject_consent.user_modified, correct_consent.user_created)

    def test_dob(self):
        hic = HicEnrollmentFactory(subject_visit=self.subject_visit_female_T0, dob=self.female_dob)
        new_dob = date(1988, 1, 1)
        age_in_years = relativedelta(self.subject_consent_female.consent_datetime, new_dob).years
        correct_consent = CorrectConsentFactory(
            subject_consent=self.subject_consent_female,
            old_dob=self.female_dob,
            new_dob=new_dob,
        )
        subject_consent = SubjectConsent.objects.get(id=self.subject_consent_female.id)
        self.assertEquals(HouseholdMember.objects.get(id=self.household_member_female_T0.id).age_in_years, age_in_years)
        self.assertEquals(EnrollmentChecklist.objects.get(id=self.enrollment_checklist_female.id).dob, new_dob)
        self.assertEquals(subject_consent.dob, new_dob)
        self.assertEquals(HicEnrollment.objects.get(subject_visit=self.subject_visit_female_T0).dob, new_dob)
        self.assertFalse(subject_consent.is_verified)
        self.assertIsNone(subject_consent.is_verified_datetime)
        self.assertIsNone(subject_consent.verified_by)
        if not correct_consent.id:
            self.assertEquals(subject_consent.user_modified, correct_consent.user_created)
            self.assertEquals(hic.user_modified, correct_consent.user_created)

    def test_gender(self):
        correct_consent = CorrectConsentFactory(
            subject_consent=self.subject_consent_female,
            old_gender='F',
            new_gender='M',
        )
        subject_consent = SubjectConsent.objects.get(id=self.subject_consent_female.id)
        self.assertEquals(HouseholdMember.objects.get(id=self.household_member_female_T0.id).gender, 'M')
        self.assertEquals(EnrollmentChecklist.objects.get(id=self.enrollment_checklist_female.id).gender, 'M')
        self.assertEquals(subject_consent.gender, 'M')
        self.assertFalse(subject_consent.is_verified)
        self.assertIsNone(subject_consent.is_verified_datetime)
        self.assertIsNone(subject_consent.verified_by)
        if not correct_consent.id:
            self.assertEquals(subject_consent.user_modified, correct_consent.user_created)

    def test_witness(self):
        self.subject_consent_female.witness_name = 'DIMO'
        self.subject_consent_female.save(update_fields=['witness_name'])
        correct_consent = CorrectConsentFactory(
            subject_consent=self.subject_consent_female,
            old_witness_name='DIMO',
            new_witness_name='BIMO',
        )
        subject_consent = SubjectConsent.objects.get(id=self.subject_consent_female.id)
        self.assertEquals(subject_consent.witness_name, 'BIMO')
        self.assertFalse(subject_consent.is_verified)
        self.assertIsNone(subject_consent.is_verified_datetime)
        self.assertIsNone(subject_consent.verified_by)
        if not correct_consent.id:
            self.assertEquals(subject_consent.user_modified, correct_consent.user_created)

    def test_to_unverify_consent(self):
        self.subject_consent_female.witness_name = 'DIMO'
        self.assertFalse(self.subject_consent_female.is_verified)
        self.assertIsNone(self.subject_consent_female.is_verified_datetime)
        self.assertIsNone(self.subject_consent_female.verified_by)
        self.subject_consent_female.is_verified = True
        self.subject_consent_female.is_verified_datetime = datetime(2016, 4, 18, 10, 3, 42, 215477)
        self.subject_consent_female.verified_by = 'ckgathi'
        self.subject_consent_female.save(update_fields=['witness_name', 'verified_by', 'is_verified_datetime', 'is_verified'])
        self.assertTrue(self.subject_consent_female.is_verified)
        self.assertEqual(self.subject_consent_female.is_verified_datetime, datetime(2016, 4, 18, 10, 3, 42, 215477))
        self.assertEqual(self.subject_consent_female.verified_by, 'ckgathi')
        correct_consent = CorrectConsentFactory(
            subject_consent=self.subject_consent_female,
            old_witness_name='DIMO',
            new_witness_name='BIMO',
        )
        subject_consent = SubjectConsent.objects.get(id=self.subject_consent_female.id)
        self.assertEquals(subject_consent.witness_name, 'BIMO')
        self.assertFalse(self.subject_consent_female.is_verified)
        self.assertIsNone(self.subject_consent_female.is_verified_datetime)
        self.assertIsNone(self.subject_consent_female.verified_by)
        if not correct_consent.id:
            self.assertEquals(subject_consent.user_modified, correct_consent.user_created)
