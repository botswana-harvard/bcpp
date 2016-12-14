# from django.utils.unittest.case import TestCase
# from django.db.models import Q
# from django.test.utils import override_settings
# 
# from bhp066.apps.member.tests.factories.household_member_factory import HouseholdMemberFactory
# from bhp066.apps.bcpp_household.tests.factories.household_structure_factory import HouseholdStructureFactory
# from edc.subject.registration.tests.factories.registered_subject_factory import RegisteredSubjectFactory
# from edc.subject.registration.models.registered_subject import RegisteredSubject
# from bhp066.apps.bcpp_household.tests.factories.household_factory import HouseholdFactory
# from bhp066.apps.bcpp_household.tests.factories.plot_factory import PlotFactory
# from bhp066.apps.member.models.household_member import HouseholdMember
# from bhp066.apps.bcpp_clinic.tests.factories.clinic_eligibility_factory import ClinicEligibilityFactory
# from bhp066.apps.bcpp_subject.classes.clinic_registered_subject_helper import ClinicRegisteredSubjectHelper
# from bhp066.apps.bcpp_clinic.tests.factories.clinic_consent_factory import ClinicConsentFactory
# from bhp066.apps.bcpp_clinic.tests.factories.clinic_visit_factory import ClinicVisitFactory
# from edc.subject.appointment.models.appointment import Appointment
# from bhp066.apps.bcpp_subject.models.subject_consent import SubjectConsent
# from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
# 
# 
# class TestUpdateClinicRegisteredSubjects(TestCase):
# 
#     app_label = 'bcpp_subject'
#     community = 'test_community'
# 
#     @override_settings(
#         SITE_CODE='01', CURRENT_COMMUNITY='test_community', CURRENT_SURVEY='bcpp-year-1',
#         CURRENT_COMMUNITY_CHECK=False,
#         LIMIT_EDIT_TO_CURRENT_SURVEY=True,
#         LIMIT_EDIT_TO_CURRENT_COMMUNITY=True,
#         FILTERED_DEFAULT_SEARCH=True,
#     )
#     def setUp(self):
# #         try:
# #             site_lab_profiles.register(BcppSubjectProfile())
# #         except AlreadyRegisteredLabProfile:
# #             pass
#         BcppAppConfiguration().prepare()
#         BcppAppConfigurat                                                            ion().prep_survey_for_tests()
# #         site_lab_tracker.autodiscover()
# #         BcppSubjectVisitSchedule().build()
# #         site_rule_groups.autodiscover()
#         for _ in range(2):
#             RegisteredSubjectFactory(identity='317918515')
# 
#         self.cregistered_subject = RegisteredSubject.objects.all()[0]
#         household_structure = HouseholdStructureFactory()
#         self.household_member = HouseholdMemberFactory(registered_subject=self.cregistered_subject, household_structure=household_structure)
# 
#         self.registered_subject = RegisteredSubject.objects.all()[1]
#         plot = PlotFactory(status='bcpp_clinic', plot_identifier='160000-00')
#         household = HouseholdFactory(plot=plot)
#         household_structure = HouseholdStructureFactory(household=household)
#         self.clinic_household_member = HouseholdMemberFactory(registered_subject=self.registered_subject, household_structure=household_structure)
#         self.clinic_helper = ClinicRegisteredSubjectHelper()
# 
#     def test_find_duplicates(self):
#         self.assertTrue(self.clinic_helper.find_duplicates())
# 
#     def test_determine_bcpp_registered_subject(self):
#         bcpp_reg = self.clinic_helper.determine_bcpp_registered_subject('317918515')
#         hhm = HouseholdMember.objects.filter(registered_subject=bcpp_reg)
#         self.assertEqual(hhm.household_structure.household.plot.status, 'residential_habitable')
# 
#     def test_clinic_household_member(self):
#         bcpp_reg = self.clinic_helper.determine_bcpp_registered_subject('317918515')
#         self.clinic_member = None
#         try:
#             self.clinic_member = HouseholdMember.objects.get(
#                 Q(registered_subject__identity=bcpp_reg.identity),
#                 Q(household_structure__household__plot__status='bcpp_clinic')
#             )
#         except HouseholdMember.DoesNotExist:
#             pass
#         self.assertTrue(self.clinic_member)
# 
#     def test_update_clinic_household_member(self):
#         bcpp_reg = self.clinic_helper.determine_bcpp_registered_subject('317918515')
#         self.clinic_member = None 
#         try:
#             self.clinic_member = HouseholdMember.objects.get(
#                 Q(registered_subject__identity=bcpp_reg.identity),
#                 Q(household_structure__household__plot__status='bcpp_clinic')
#             )
#             self.assertNotEqual(self.clinic_member.registered_subject.id, bcpp_reg.id)
#         except HouseholdMember.DoesNotExist:
#             pass
# 
#         self.clinic_helper.update_clinic_household_member(bcpp_reg)
#         try:
#             self.clinic_member = HouseholdMember.objects.get(
#                 Q(registered_subject__identity=bcpp_reg.identity),
#                 Q(household_structure__household__plot__status='bcpp_clinic')
#             )
#             self.assertEqual(self.clinic_member.registered_subject.id, bcpp_reg.id)
#         except HouseholdMember.DoesNotExist:
#             pass
# 
#     def test_update_clinic_appointment(self):
#         self.clinic_eligibility = ClinicEligibilityFactory(
#             household_member=self.clinic_household_member,
#             identity='317918515',
#         )
#         self.clinic_consent = ClinicConsentFactory(
#             registered_subject=self.cregistered_subject,
#             identity='317918515',
#         )
#         self.clinic_visit = ClinicVisitFactory(
#             subject_identifier=self.cregistered_subject.subject_identifier
#         )
#         appointment = Appointment.history.filter(
#             registered_subject__identity=self.cregistered_subject.identity,
#             visit_definition__code='C0')
#         self.assertEqual(1, appointment.count())
#         self.assertNotEqual(appointment[0].registered_subject.id, self.registered_subject.id)
#         self.clinic_helper.update_clinic_appointment(self.registered_subject)
#         self.assertEqual(appointment[0].registered_subject.id, self.registered_subject.id)
# 
#     def test_update_clinic_consent(self):
#         self.clinic_eligibility = ClinicEligibilityFactory(
#                 household_member=self.clinic_household_member,
#                 identity='317918515',
#         )
#         self.clinic_consent = ClinicConsentFactory(
#               registered_subject=self.cregistered_subject,
#               identity='317918515',
#         )
#         self.clinic_consent = SubjectConsent.objects.filter(registered_subject__identity=self.registered_subject.identity)
#         self.assertEqual(1, self.clinic_consent.count())
#     