from django.test import TestCase
from django.utils import timezone

from datetime import timedelta, datetime

from ..models import PimaVl

from datetime import date
from dateutil.relativedelta import relativedelta


from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc.core.bhp_variables.models import StudySite

from bhp066.apps.bcpp_household.models import HouseholdStructure
from bhp066.apps.bcpp_household.tests.factories import PlotFactory, RepresentativeEligibilityFactory
from bhp066.apps.member.tests.factories import HouseholdMemberFactory, EnrollmentChecklistFactory
from bhp066.apps.bcpp_survey.models import Survey

from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile

from .factories import SubjectConsentFactory, SubjectVisitFactory


from edc_quota.client.models import Quota
from edc_quota.client.exceptions import QuotaReachedError
from edc.map.classes.controller import site_mappers


class TestPimaVL(TestCase):

    app_label = 'bcpp_subject'
    community = 'test_community'

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

        plot = PlotFactory(community=self.community, household_count=1, status='residential_habitable')

        survey = Survey.objects.all().order_by('datetime_start')[0]

        self.study_site = StudySite.objects.get(site_code='01')

        self.household_structure = HouseholdStructure.objects.get(household__plot=plot, survey=survey)
        RepresentativeEligibilityFactory(household_structure=self.household_structure)
        HouseholdMemberFactory(household_structure=self.household_structure)

        self.male_dob = date.today() - relativedelta(years=25)
        self.male_age_in_years = 25
        self.male_first_name = 'ERIK'
        self.male_initials = "EW"
        female_dob = date.today() - relativedelta(years=35)
        female_age_in_years = 35
        female_first_name = 'ERIKA'
        female_initials = "EW"

        self.household_member_female_T0 = HouseholdMemberFactory(
            household_structure=self.household_structure, gender='F',
            age_in_years=female_age_in_years,
            first_name=female_first_name,
            initials=female_initials
        )
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

        EnrollmentChecklistFactory(
            household_member=self.household_member_female_T0,
            gender='F',
            citizen='Yes',
            dob=female_dob,
            guardian='No',
            initials=self.household_member_female_T0.initials,
            part_time_resident='Yes'
        )

        subject_consent_female = SubjectConsentFactory(
            household_member=self.household_member_female_T0, study_site=self.study_site, gender='F',
            dob=female_dob, first_name=female_first_name, initials=female_initials)
        self.subject_consent_male = SubjectConsentFactory(
            household_member=self.household_member_male_T0, study_site=self.study_site,
            gender='M', dob=self.male_dob, first_name=self.male_first_name, initials=self.male_initials)

        self.registered_subject_male = RegisteredSubject.objects.get(
            subject_identifier=self.subject_consent_male.subject_identifier)
        self.registered_subject_female = RegisteredSubject.objects.get(
            subject_identifier=subject_consent_female.subject_identifier)

        self.appointment_male_T0 = Appointment.objects.get(
            registered_subject=self.registered_subject_male, visit_definition__code='T0')
        self.appointment_female_T0 = Appointment.objects.get(
            registered_subject=self.registered_subject_female, visit_definition__code='T0')

        self.subject_visit_male_T0 = SubjectVisitFactory(
            appointment=self.appointment_male_T0, household_member=self.household_member_male_T0)
        self.subject_visit_female_T0 = SubjectVisitFactory(
            appointment=self.appointment_female_T0, household_member=self.household_member_female_T0)

        Quota.objects.create(
            app_label='bcpp_subject',
            model_name='PimaVl',
            target=1,
            start_date=timezone.now().date(),
            expiration_date=timezone.now().date() + timedelta(days=1)
        )
        self.assertEqual(1, Quota.objects.all().count())

    def test_within_quota(self):
        """Asserts mixin save method works with model save."""
        self.create_pimavl(1, self.subject_visit_male_T0)
        self.assertEqual(1, PimaVl.objects.all().count())

    def test_quota_reached(self):
        """Asserts mixin save method works with model save."""
        self.create_pimavl(1, self.subject_visit_male_T0)
        self.assertEqual(1, PimaVl.objects.all().count())
        self.assertRaises(QuotaReachedError, self.create_pimavl(2, self.subject_visit_female_T0))

    def test_quota_reached_override(self):
        """Asserts mixin save method works with model save."""
        self.create_pimavl(1, self.subject_visit_male_T0)
        self.assertEqual(1, PimaVl.objects.all().count())
        #
        self.create_pimavl(2, self.subject_visit_female_T0, 'V7D8N', 'DR2AW')
        self.assertEqual(1, PimaVl.objects.all().count())

    def create_pimavl(self, pima_id, subject_visit, override_key=None, confirmation_code=None):
        """ """
        try:
            PimaVl(
                report_datetime=datetime.today(), poc_vl_today='Yes', poc_vl_type='Mobile settings',
                time_of_test=datetime.today(), time_of_result=datetime.today(),
                easy_of_use='easy', pima_id='pima_id{0}'.format(pima_id), poc_vl_value=1000,
                subject_visit=subject_visit
            ).save()
        except QuotaReachedError:
            return PimaVl.objects.create
