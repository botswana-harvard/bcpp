from datetime import datetime, timedelta, date
from django.conf import settings

from django.test import TestCase
from django.test.utils import override_settings
from dateutil.relativedelta import relativedelta

from edc_constants.constants import NEW, NOT_REQUIRED, KEYED, YES, NO
from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc.core.bhp_variables.models import StudySite
from edc.subject.registration.tests.factories import RegisteredSubjectFactory

from bhp066.apps.bcpp_household.models import HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory, RepresentativeEligibilityFactory
from bhp066.apps.member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.member.classes import EnumerationHelper
from bhp066.apps.member.models import HouseholdMember
from bhp066.apps.bcpp_survey.models import Survey

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_lab.tests.factories import SubjectRequisitionFactory
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
from bhp066.apps.bcpp_lab.models import AliquotType, Panel

from bhp066.apps.bcpp_subject.models import HivResult

from .factories import (SubjectConsentFactory, SubjectVisitFactory)


class BaseRuleGroupTestSetup(TestCase):
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
        BcppAppConfiguration().prepare()
        site_lab_tracker.autodiscover()
        BcppSubjectVisitSchedule().build()
        site_rule_groups.autodiscover()
        BcppAppConfiguration().prep_survey_for_tests()

        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')

        survey_T0 = Survey.objects.get(survey_slug='bcpp-year-1')
        survey_T1 = Survey.objects.get(survey_slug='bcpp-year-2')
        survey_T2 = Survey.objects.get(survey_slug='bcpp-year-3')

        self.study_site = StudySite.objects.get(site_code='01')

        self.household_structure = HouseholdStructure.objects.get(household__plot=plot, survey=survey_T0)
        self.household_structure_y2 = HouseholdStructure.objects.get(household__plot=plot, survey=survey_T1)
        self.household_structure_y3 = HouseholdStructure.objects.get(household__plot=plot, survey=survey_T2)

        for j in range(3):
            RepresentativeEligibilityFactory(
                household_structure=HouseholdStructure.objects.get(household__plot=plot, survey=surveys[j]))

        for _ in range(3):
            HouseholdMemberFactory(household_structure=self.household_structure)
        RepresentativeEligibilityFactory(household_structure=self.household_structure)
        RepresentativeEligibilityFactory(household_structure=self.household_structure_y2)
        RepresentativeEligibilityFactory(household_structure=self.household_structure_y3)
        HouseholdMemberFactory(household_structure=self.household_structure)
        #HouseholdMemberFactory(household_structure=self.household_structure)
        #HouseholdMemberFactory(household_structure=self.household_structure)

        male_dob = date.today() - relativedelta(years=25)
        male_age_in_years = 25
        male_first_name = 'ERIK'
        male_initials = "EW"

        self.household_member_male_T0 = self.new_household_member(
            male_dob, male_age_in_years, male_first_name, male_initials, 'M')

        female_dob = date.today() - relativedelta(years=35)
        female_age_in_years = 35
        female_first_name = 'ERIKA'
        female_initials = "EW"

        self.household_member_female_T0 = self.new_household_member(
            female_dob, female_age_in_years, female_first_name, female_initials, 'F')

        registered_subject = RegisteredSubjectFactory(registration_identifier='123456467')
        self.household_member_female_T0 = HouseholdMemberFactory(
            household_structure=self.household_structure, gender='F', age_in_years=female_age_in_years,
            first_name=female_first_name, initials=female_initials, registered_subject=registered_subject)
        registered_subject = RegisteredSubjectFactory(registration_identifier='123456468')
        self.household_member_male_T0 = HouseholdMemberFactory(
            household_structure=self.household_structure, gender='M',
            age_in_years=male_age_in_years, first_name=male_first_name,
            initials=male_initials, registered_subject=registered_subject)
        self.household_member_female_T0.member_status = 'BHS_SCREEN'
        self.household_member_male_T0.member_status = 'BHS_SCREEN'
        self.household_member_female_T0.save()
        self.household_member_male_T0.save()

        self.new_enrollment_checklist(self.household_member_female_T0, female_dob)

        self.new_enrollment_checklist(self.household_member_male_T0, male_dob)

        subject_consent_female = SubjectConsentFactory(
            household_member=self.household_member_female_T0, confirm_identity='101129811', identity='101129811',
            study_site=self.study_site, gender='F',
            dob=female_dob, first_name=female_first_name,
            initials=female_initials)

        subject_consent_male = SubjectConsentFactory(
            household_member=self.household_member_male_T0,
            confirm_identity='101119811', identity='101119811',
            study_site=self.study_site, gender='M', dob=male_dob,
            first_name=male_first_name, initials=male_initials)

        self.assertEqual(HouseholdStructure.objects.filter(
            household=self.household_structure.household, survey=survey_T0, enumerated=True, enrolled=True).count(), 1)

        enumeration_helper_T2 = EnumerationHelper(self.household_structure.household, survey_T0, survey_T1)
        enumeration_helper_T2.add_members_from_survey()
        self.household_member_female = HouseholdMember.objects.get(
            internal_identifier=self.household_member_female_T0.internal_identifier,
            household_structure__survey=survey_T1)
        self.household_member_male = HouseholdMember.objects.get(
            internal_identifier=self.household_member_male_T0.internal_identifier,
            household_structure__survey=survey_T1)
        self.assertEqual(HouseholdStructure.objects.filter(
            household=self.household_structure_y2.household, 
            survey=survey_T1, enumerated=True, enrolled=True).count(), 1)

        enumeration_helper_T3 = EnumerationHelper(self.household_structure.household, survey_T1, survey_T2)
        enumeration_helper_T3.add_members_from_survey()
        self.household_member_female_T2 = HouseholdMember.objects.get(
            internal_identifier=self.household_member_female.internal_identifier,
            household_structure__survey=survey_T2)
        self.household_member_male_T2 = HouseholdMember.objects.get(
            internal_identifier=self.household_member_male.internal_identifier,
            household_structure__survey=survey_T2)
        self.assertEqual(HouseholdStructure.objects.filter(
            household=self.household_structure_y3.household,
            survey=survey_T2, enumerated=True, enrolled=True).count(), 1)

        self.registered_subject_female = RegisteredSubject.objects.get(
            subject_identifier=subject_consent_female.subject_identifier)
        self.registered_subject_male = RegisteredSubject.objects.get(
            subject_identifier=subject_consent_male.subject_identifier)
        self.appointment_female = Appointment.objects.get(
            registered_subject=self.registered_subject_female, visit_definition__code='T1')
        self.appointment_female_T0 = Appointment.objects.get(
            registered_subject=self.registered_subject_female, visit_definition__code='T0')
        self.appointment_female_T2 = Appointment.objects.get(
            registered_subject=self.registered_subject_female, visit_definition__code='T2')
        self.subject_visit_female_T0 = SubjectVisitFactory(
            appointment=self.appointment_female_T0, household_member=self.household_member_female_T0)
        self.subject_visit_female = SubjectVisitFactory(
            appointment=self.appointment_female, household_member=self.household_member_female)
        self.subject_visit_female_T2 = SubjectVisitFactory(
            appointment=self.appointment_female_T2, household_member=self.household_member_female_T2)
        self.appointment_male = Appointment.objects.get(
            registered_subject=self.registered_subject_male, visit_definition__code='T1')
        self.appointment_male_T0 = Appointment.objects.get(
            registered_subject=self.registered_subject_male, visit_definition__code='T0')
        self.appointment_male_T2 = Appointment.objects.get(
            registered_subject=self.registered_subject_male, visit_definition__code='T2')
        self.subject_visit_male_T0 = SubjectVisitFactory(
            appointment=self.appointment_male_T0, household_member=self.household_member_male_T0)
        self.subject_visit_male = SubjectVisitFactory(
            appointment=self.appointment_male, household_member=self.household_member_male)
        self.subject_visit_male_T2 = SubjectVisitFactory(
            appointment=self.appointment_male_T2, household_member=self.household_member_male_T2)

    def new_household_member(self, dob, age, first_name, initials, gender):
        return HouseholdMemberFactory(
            household_structure=self.household_structure,
            gender=gender, age_in_years=age,
            first_name=first_name, initials=initials)

    def new_enrollment_checklist(self, household_member, dob):
        EnrollmentChecklistFactory(
            household_member=household_member,
            gender=household_member.gender,
            citizen=YES,
            dob=dob,
            guardian=NO,
            initials=household_member.initials,
            part_time_resident=YES)

    def check_male_registered_subject_rule_groups(self, subject_visit):
        circumsition_options = {}
        circumsition_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='circumcision',
            appointment=subject_visit.appointment)

        circumcised_options = {}
        circumcised_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='circumcised',
            appointment=subject_visit.appointment)

        uncircumcised_options = {}
        uncircumcised_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='uncircumcised',
            appointment=subject_visit.appointment)

        reproductivehealth_options = {}
        reproductivehealth_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='reproductivehealth',
            appointment=subject_visit.appointment)

        pregnancy_options = {}
        pregnancy_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pregnancy',
            appointment=subject_visit.appointment)

        nonpregnancy_options = {}
        nonpregnancy_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='nonpregnancy',
            appointment=subject_visit.appointment)

        if subject_visit == self.subject_visit_male_T0:
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **circumsition_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **circumcised_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(
                entry_status=NEW, **uncircumcised_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(
                entry_status=NOT_REQUIRED, **reproductivehealth_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(
                entry_status=NOT_REQUIRED, **pregnancy_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(
                entry_status=NOT_REQUIRED, **nonpregnancy_options).count(), 1)
        else:
            self.assertEqual(ScheduledEntryMetaData.objects.filter(
                entry_status=NEW, **reproductivehealth_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **pregnancy_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **nonpregnancy_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(
                entry_status=NOT_REQUIRED, **circumsition_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(
                entry_status=NOT_REQUIRED, **circumcised_options).count(), 1)
            self.assertEqual(ScheduledEntryMetaData.objects.filter(
                entry_status=NOT_REQUIRED, **uncircumcised_options).count(), 1)

    def new_metadata_is_not_keyed(self):
        self.assertEquals(ScheduledEntryMetaData.objects.filter(
            entry_status=KEYED, appointment=self.subject_visit_male.appointment).count(), 0)
        self.assertEquals(
            RequisitionMetaData.objects.filter(
                entry_status=KEYED, appointment=self.subject_visit_male.appointment).count(), 0)

    @property
    def baseline_subject_visit(self):
        """ Return baseline subject visit"""
        self.subject_visit_male_T0.delete()
        self.subject_visit_male_T0 = SubjectVisitFactory(
            appointment=self.appointment_male_T0, household_member=self.household_member_male_T0)
        self.check_male_registered_subject_rule_groups(self.subject_visit_male_T0)
        return self.subject_visit_male_T0

    @property
    def annual_subject_visit_y2(self):
        """ Return annuall subject visit """
        self.subject_visit_male.delete()
        self.assertEqual(
            ScheduledEntryMetaData.objects.filter(appointment=self.appointment_male).count(), 0)
        self.subject_visit_male = SubjectVisitFactory(
            appointment=self.appointment_male, household_member=self.household_member_male)
        return self.subject_visit_male

    @property
    def annual_subject_visit_y3(self):
        """ Return annuall subject visit """
        self.subject_visit_male_T2.delete()
        self.assertEqual(
            ScheduledEntryMetaData.objects.filter(appointment=self.appointment_male_T2).count(), 0)
        self.subject_visit_male_T2 = SubjectVisitFactory(
            appointment=self.appointment_male_T2, household_member=self.household_member_male_T2)
        return self.subject_visit_male_T2

    def hiv_result(self, status, subject_visit):
        """ Create HivResult for a particular survey"""
        aliquot_type = AliquotType.objects.all()[0]
        site = StudySite.objects.all()[0]
        microtube_panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=subject_visit, panel=microtube_panel, aliquot_type=aliquot_type, site=site)

        self._hiv_result = HivResult.objects.create(
            subject_visit=subject_visit,
            hiv_result=status,
            report_datetime=datetime.today(),
            insufficient_vol=NO
        )
        return self._hiv_result
