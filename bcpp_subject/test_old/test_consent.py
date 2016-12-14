# from datetime import datetime
# from dateutil.relativedelta import relativedelta
# from django.db import IntegrityError
# from django.test import TestCase
# 
# from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
# from edc.core.bhp_content_type_map.models import ContentTypeMap
# from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
# from edc.core.identifier.exceptions import IdentifierError
# from edc.subject.lab_tracker.classes import site_lab_tracker
# from edc.subject.registration.models import RegisteredSubject
# 
# from bhp066.apps.bcpp_dashboard.classes import HouseholdDashboard
# from bhp066.apps.bcpp_dashboard.tests.dashboard_tests import setup_dashboard
# from bhp066.apps.bcpp_household.models import HouseholdStructure, Household
# from bhp066.apps.member.models import HouseholdMember
# from bhp066.apps.member.tests.factories import HouseholdMemberFactory
# from bhp066.apps.bcpp_subject.tests.factories import SubjectConsentFactory
# from bhp066.apps.bcpp_survey.models import Survey
# 
# from ..models import SubjectConsent
# 
# 
# class TestConsent(TestCase):
# 
#     app_label = 'bcpp_subject'
# 
#     def test_p1(self):
#         self.assertTrue(Household.objects.all().count() == 0)
#         self.assertTrue(HouseholdStructure.objects.all().count() == 0)
#         self.assertTrue(HouseholdMember.objects.all().count() == 0)
#         site_lab_tracker.autodiscover()
#         study_specific = StudySpecificFactory()
#         StudySiteFactory()
# 
#         content_type_map_helper = ContentTypeMapHelper()
#         content_type_map_helper.populate()
#         content_type_map_helper.sync()
#         content_type_map = ContentTypeMap.objects.get(model__iexact=SubjectConsent._meta.object_name)
#         setup_dashboard(self)  # creates 3 surveys a plot and two HH which -> 6 HHS
# 
#         print 'initialize the HH dashboard which will create HHS'
#         print 'assert no survey for today\'s date'
#         self.survey1.datetime_end = datetime.today() + relativedelta(days=-5)
#         self.survey1.save()
#         self.assertRaises(TypeError, HouseholdDashboard, self.dashboard_type, self.dashboard_id, self.dashboard_model)
#         self.assertEquals(HouseholdStructure.objects.all().count(), 6)
#         print 'update survey1 to include today'
#         self.survey1.datetime_end = datetime.today() + relativedelta(days=+5)
#         self.survey1.save()
#         print 'try again, initialize the HH dashboard which will create HHS'
#         self.household_dashboard = HouseholdDashboard(self.dashboard_type, self.dashboard_id, self.dashboard_model)
#         print 'assert household structure exists for this HH and the three surveys'
#         self.assertEquals(HouseholdStructure.objects.filter(household=self.household1).count(), 3)
#         self.household_structure = self.household_dashboard.get_household_structure()
#         print 'create another new HH in community {0}.'.format(self.community)
#         self.assertEquals(HouseholdStructure.objects.filter(household=self.household2).count(), 3)
#         print 'assert no additional hh structure created'
#         self.assertEquals(HouseholdStructure.objects.all().count(), 6)  # 2 surveys for each HH = 2 x 3 = 6
#         print 'create HH members for this survey and HH {0}'.format(self.household1)
#         self.household_member1 = HouseholdMemberFactory(household_structure=self.household_structure)
#         print 'household_member1.registered_subject.pk = {0}'.format(self.household_member1.registered_subject.pk)
#         print 'household_member1.survey = {0}'.format(self.household_member1.survey)
#         self.household_member2 = HouseholdMemberFactory(household_structure=self.household_structure)
#         print self.household_member2.registered_subject.pk
#         self.household_member3 = HouseholdMemberFactory(household_structure=self.household_structure)
#         print self.household_member3.registered_subject.pk
#         self.household_member4 = HouseholdMemberFactory(household_structure=self.household_structure)
#         print self.household_member4.registered_subject.pk
# 
#         # this consent has a fk to registered subject
#         # confirm that the signals do not create more than one registered
#         # subject or anything like that. consent.rs must equal household_member.rs, etc
# 
#         self.assertEqual(Survey.objects.all().count(), 3)
#         print 'assert one RS per HM'
#         self.assertEqual(HouseholdMember.objects.all().count(), RegisteredSubject.objects.all().count())
#         print 'assert HM1.registered_subject.subject_identifier is a pk (not consented yet)'
#         self.assertRegexpMatches(HouseholdMember.objects.get(pk=self.household_member1.pk).registered_subject.subject_identifier, self.re_pk)
#         print 'consent household_member1'
#         consent1 = SubjectConsentFactory(household_member=self.household_member1)
#         self.assertEqual(Survey.objects.all().count(), 3)
#         print consent1.subject_identifier
#         print HouseholdMember.objects.get(pk=self.household_member1.pk).registered_subject.subject_identifier
#         print 'assert consent1 household member is household_member1'
#         print self.assertEqual(consent1.household_member.pk, self.household_member1.pk)
#         print 'assert still one RS per HM'
#         self.assertEqual(HouseholdMember.objects.all().count(), RegisteredSubject.objects.all().count())
#         print 'assert subject identifier on consent1 == subject identifier in registered_subject'
#         self.assertEqual(consent1.subject_identifier, RegisteredSubject.objects.get(subject_identifier=consent1.subject_identifier).subject_identifier)
#         print 'assert consent1 registered subject pk = household_member1 registered subject pk'
#         self.assertEqual(consent1.registered_subject.pk, HouseholdMember.objects.get(pk=self.household_member1.pk).registered_subject.pk)
#         print 'assert consent1 registered subject subject identifier = household_member1 registered subject subject_identifier'
#         self.assertEqual(consent1.registered_subject.subject_identifier, HouseholdMember.objects.get(pk=self.household_member1.pk).registered_subject.subject_identifier)
#         print 'assert cannot create a second consent for consented household_member1 {0}'.format(self.household_member1.survey)
#         self.assertRaises(IdentifierError, SubjectConsentFactory, household_member=self.household_member1)
# 
#         # repeat for year 2, make a household_structure, members and consent, etc.
#         # verify FK constraints do not prevent member, consent data
#         # verify that subsequent surveys refer to the same registered subject
#         # that being the one created from the first year
# 
#         print 'repeat for YEAR 2 for household1'
#         print 'assert still have only 3 surveys'
#         self.assertEqual(Survey.objects.all().count(), 3)
#         print 'assert have 4 HHMs for household1 (from survey1'
#         self.assertEqual(HouseholdMember.objects.all().count(), 4)
#         print 'get a household dashboard for survey2 using HH2'
#         self.dashboard_type = 'household'
#         self.dashboard_model = 'household'
#         self.dashboard_id = self.household1.pk
#         print 'instantiate hHH dashboard with household'
#         household_dashboard_survey2 = HouseholdDashboard(self.dashboard_type, self.dashboard_id, self.dashboard_model, survey=self.survey2)
#         print household_dashboard_survey2
#         self.assertEqual(Survey.objects.all().count(), 3)
#         print 'assert defaults to survey1, HHS for survey1'
#         self.assertEqual(household_dashboard_survey2.get_survey(), self.survey1)
#         self.assertEqual(household_dashboard_survey2.get_household_structure().survey, self.survey1)
#         print 'get a household dashboard for survey2 using HH2'
#         self.household_structure2 = HouseholdStructure.objects.get(household=self.household1, survey=self.survey2)
#         self.dashboard_type = 'household'
#         self.dashboard_model = 'household_structure'
#         self.dashboard_id = self.household_structure2.pk
#         household_dashboard_survey2 = HouseholdDashboard(self.dashboard_type, self.dashboard_id, self.dashboard_model, survey=self.survey2)
#         household_dashboard_survey2
#         print 'confirm uses HHS2 and survey2'
#         self.assertEqual(household_dashboard_survey2.get_survey(), self.survey2)
#         self.assertEqual(household_dashboard_survey2.get_household_structure().survey, self.survey2)
#         household_structure = household_dashboard_survey2.get_household_structure()
#         self.assertEqual(Survey.objects.all().count(), 3)
#         print 'assert household dashboard returns correct household structure if given survey2'
#         self.assertEqual(household_structure.survey.pk, self.survey2.pk)
#         print 'assert household dashboard returns correct household structure if given HH1'
#         self.assertEqual(household_structure.household.pk, self.household1.pk)
#         print 'household_structure={0}, plot={1}'.format(household_structure, household_structure.plot)
#         print 'assert have 4 HHMs imported from first survey after instantiating dashboard'
#         household_dashboard_survey2.get_context()
#         self.assertEqual(HouseholdMember.objects.filter(household_structure=household_structure).count(), 4)
#         print 'assert cannot create a household_member for this survey for known household members (because the dashboard created them)'
#         self.assertRaises(IntegrityError, HouseholdMemberFactory, household_structure=household_structure, survey=self.survey2, registered_subject=self.household_member1.registered_subject)
#         self.assertRaises(IntegrityError, HouseholdMemberFactory, household_structure=household_structure, survey=self.survey2, registered_subject=self.household_member2.registered_subject)
#         self.assertRaises(IntegrityError, HouseholdMemberFactory, household_structure=household_structure, survey=self.survey2, registered_subject=self.household_member3.registered_subject)
#         self.assertRaises(IntegrityError, HouseholdMemberFactory, household_structure=household_structure, survey=self.survey2, registered_subject=self.household_member4.registered_subject)
# 
#         # in BCPP, subject consent has a key to registered subject as does
#         # household member. ensure both are pointing to the same registered_subject
#         # not only for this survey but always. a household_member is created anew
#         # for each survey but still refers to a common registered subject. the same
#         # for the consent, a new consent for each survey but pointing to the same
#         # registered_subject. household_member uses the registered_subject internal
#         # identifier field to figure out which registered subject to use when
#         # setting the attribute for subsequent surveys.
# 
#         print 'get a list of household members for the survey2 household dashboard'
#         household_members = household_dashboard_survey2.get_household_members_as_list()
#         household_member1 = household_members[0]
#         print 'assert 8 household members'
#         self.assertEqual(HouseholdMember.objects.all().count(), 8)
#         print '... 4 for survey 1 and 4 for survey 2'
#         self.assertEqual(HouseholdMember.objects.filter(survey=self.survey1).count(), 4)
#         self.assertEqual(HouseholdMember.objects.filter(survey=self.survey2).count(), 4)
#         print 'assert still 4 registered subjects'
#         self.assertEqual(RegisteredSubject.objects.all().count(), 4)
#         print 'assert one RS per 2 HM'
#         self.assertEqual(HouseholdMember.objects.all().count(), RegisteredSubject.objects.all().count() * 2)
#         print 'assert HM1.registered_subject.subject_identifier is a subject identifier (was consented in previous survey)'
#         print HouseholdMember.objects.get(pk=household_member1.pk).registered_subject.subject_identifier
#         print HouseholdMember.objects.get(pk=household_member1.pk).registered_subject.subject_identifier_as_pk
#         self.assertTrue(HouseholdMember.objects.get(pk=household_member1.pk).registered_subject.subject_identifier.startswith('066'))
#         print 'consent household_member1 (it should find the existing registered subject and subject identifier)'
#         consent1 = SubjectConsentFactory(household_member=household_member1)
#         print consent1.subject_identifier
#         print HouseholdMember.objects.get(pk=household_member1.pk).registered_subject.subject_identifier
#         print 'assert consent1 household member is household_member1'
#         print self.assertEqual(consent1.household_member.pk, household_member1.pk)
#         print 'assert still one RS per HM'
#         self.assertEqual(HouseholdMember.objects.all().count(), RegisteredSubject.objects.all().count() * 2)
#         print 'assert subject identifier on consent1 == subject identifier in registered_subject'
#         self.assertEqual(consent1.subject_identifier, RegisteredSubject.objects.get(subject_identifier=consent1.subject_identifier).subject_identifier)
#         print 'assert consent1 registered subject pk = household_member1 registered subject pk'
#         self.assertEqual(consent1.registered_subject.pk, HouseholdMember.objects.get(pk=household_member1.pk).registered_subject.pk)
#         print 'assert consent1 registered subject subject identifier = household_member1 registered subject subject_identifier'
#         self.assertEqual(consent1.registered_subject.subject_identifier, HouseholdMember.objects.get(pk=household_member1.pk).registered_subject.subject_identifier)
#         print 'assert consent1 registered subject pk = household_member1 registered subject pk for previous survey'
#         self.assertEqual(consent1.registered_subject.pk, HouseholdMember.objects.get(pk=self.household_member1.pk).registered_subject.pk)
