# from __future__ import print_function
#
# from datetime import datetime
# from dateutil.relativedelta import relativedelta
#
# from django import forms
# from django.core.exceptions import ValidationError
# from django.test import TestCase
#
# from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
# from edc_map.classes import Mapper, site_mappers
#
# from bhp066.apps.bcpp_household.models import HouseholdStructure
# from bhp066.apps.bcpp_household.tests.factories import PlotFactory
# from bhp066.apps.member.tests.factories import HouseholdMemberFactory
# from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory
#
# from ..forms import SubjectConsentForm
#
# from .factories import SubjectConsentFactory
#
#
# class TestPlotMapper(Mapper):
#     map_area = 'test_community2'
#     map_code = '099'
#     regions = []
#     sections = []
#     landmarks = []
#     gps_center_lat = -25.033194
#     gps_center_lon = 25.747132
#     radius = 5.5
#     location_boundary = ()
#
# site_mappers.register(TestPlotMapper)
#
#
# class TestForms(TestCase):
#
#     def setUp(self):
#         StudySpecificFactory()
#         StudySiteFactory()
#         self.survey = SurveyFactory()
#         self.plot = PlotFactory(community='test_community2', household_count=1, status='occupied')
#         self.household_structure = HouseholdStructure.objects.get(household__plot=self.plot)
#         self.household_member = HouseholdMemberFactory(household_structure=self.household_structure)
#
#     def test_subject_consent_form1(self):
#         """Cannot consent if household_member.eligible_subject = False."""
#         self.household_member.eligible_subject = False
#         self.assertRaisesRegexp(
#             ValidationError, 'Subject\ is\ not\ eligible',
#             SubjectConsentFactory, household_member=self.household_member)
#         data = {'household_member': self.household_member}
#         subject_consent_form = SubjectConsentForm()
#         subject_consent_form.cleaned_data = data
#         self.assertRaisesRegexp(forms.ValidationError, 'Subject\ is\ not\ eligible', subject_consent_form.clean)
#
#     def test_subject_consent_form2(self):
#         """Minor cannot consent if no guardian name."""
#         self.household_member.eligible_subject = True
#         data = {'household_member': self.household_member,
#                 'is_minor': 'Yes'}
#         subject_consent_form = SubjectConsentForm()
#         subject_consent_form.cleaned_data = data
#         self.assertRaisesRegexp(
#             forms.ValidationError,
#             'subject\ is\ a\ minor\ but\ have\ not\ provided\ the\ guardian\'s\ name', subject_consent_form.clean)
#
#     def test_subject_consent_form3(self):
#         """Non-Minor cannot consent if has guardian name."""
#         self.household_member.eligible_subject = True
#         data = {'household_member': self.household_member,
#                 'is_minor': 'No',
#                 'guardian_name': 'JOHNSON'}
#         subject_consent_form = SubjectConsentForm()
#         subject_consent_form.cleaned_data = data
#         self.assertRaisesRegexp(forms.ValidationError,
#                                 'subject\ is\ NOT\ a\ minor.\ Guardian\'s\ name\ is\ not\ required',
#                                 subject_consent_form.clean)
#
#     def test_subject_consent_form4(self):
#         """Cannot consent if too young (<16y)."""
#         self.household_member.eligible_subject = True
#         data = {'household_member': self.household_member,
#                 'is_minor': 'Yes',
#                 'guardian_name': 'JOHNSON',
#                 'consent_datetime': datetime.today(),
#                 'dob': datetime.today()}
#         subject_consent_form = SubjectConsentForm()
#         subject_consent_form.cleaned_data = data
#         self.assertRaisesRegexp(forms.ValidationError, 'Subject is too young to consent', subject_consent_form.clean)
#         self.household_member.eligible_subject = True
#         data = {'household_member': self.household_member,
#                 'is_minor': 'No',
#                 'consent_datetime': datetime.today(),
#                 'dob': datetime.today()}
#         subject_consent_form = SubjectConsentForm()
#         subject_consent_form.cleaned_data = data
#         self.assertRaisesRegexp(forms.ValidationError, 'Subject is too young to consent', subject_consent_form.clean)
#
#     def test_subject_consent_form5(self):
#         """Fails if minor by age but minor=No."""
#         self.household_member.eligible_subject = True
#         data = {'household_member': self.household_member,
#                 'is_minor': 'No',
#                 'guardian_name': 'JOHNSON',
#                 'consent_datetime': datetime.today(),
#                 'dob': datetime.today() + relativedelta(years=-17)}
#         subject_consent_form = SubjectConsentForm()
#         subject_consent_form.cleaned_data = data
#         self.assertRaisesRegexp(forms.ValidationError,
#                                 'subject\ is\ NOT\ a\ minor.\ Guardian\'s\ name\ is\ not\ required',
#                                 subject_consent_form.clean)
#
#     def test_subject_consent_form6(self):
#         """Fails if not minor by age but minor=Yes."""
#         self.household_member.eligible_subject = True
#         data = {'household_member': self.household_member,
#                 'is_minor': 'Yes',
#                 'consent_datetime': datetime.today(),
#                 'dob': datetime.today() + relativedelta(years=-17)}
#         subject_consent_form = SubjectConsentForm()
#         subject_consent_form.cleaned_data = data
#         self.assertRaisesRegexp(forms.ValidationError,
#                                 'subject is a minor but have not provided the guardian\'s name',
#                                 subject_consent_form.clean)
#
#     def test_subject_consent_form7(self):
#         """Fails if subject is too old."""
#         self.household_member.eligible_subject = True
#         data = {'household_member': self.household_member,
#                 'is_minor': 'Yes',
#                 'guardian_name': 'JOHNSON',
#                 'consent_datetime': datetime.today(),
#                 'dob': datetime.today() + relativedelta(years=-99)}
#         subject_consent_form = SubjectConsentForm()
#         subject_consent_form.cleaned_data = data
#         self.assertRaisesRegexp(forms.ValidationError, 'Subject is too old', subject_consent_form.clean)
#
#     def test_subject_consent_form8(self):
#         """Fails if not minor by age but minor=Yes and guardian name provided."""
#         self.household_member.eligible_subject = True
#         data = {'household_member': self.household_member,
#                 'is_minor': 'Yes',
#                 'guardian_name': 'JOHNSON',
#                 'consent_datetime': datetime.today(),
#                 'dob': datetime.today() + relativedelta(years=-17)}
#         subject_consent_form = SubjectConsentForm()
#         subject_consent_form.cleaned_data = data
#         self.assertRaisesRegexp(forms.ValidationError, 'Identity cannot be None', subject_consent_form.clean)
#
#     def test_subject_consent_form9(self):
#         """Identify and confirmation must match."""
#         self.household_member.eligible_subject = True
#         data = {'household_member': self.household_member,
#                 'is_minor': 'Yes',
#                 'guardian_name': 'JOHNSON',
#                 'consent_datetime': datetime.today(),
#                 'dob': datetime.today() + relativedelta(years=-17),
#                 'identity_type': 'omang',
#                 'identity': '123456789',
#                 'confirm_identity': '123456780'}
#         subject_consent_form = SubjectConsentForm()
#         subject_consent_form.cleaned_data = data
#         self.assertRaisesRegexp(forms.ValidationError, 'Identity numbers do not match', subject_consent_form.clean)
#
#     def test_subject_consent_form10(self):
#         """Identify and confirmation must match."""
#         self.household_member.eligible_subject = True
#         data = {'household_member': self.household_member,
#                 'is_minor': 'Yes',
#                 'guardian_name': 'JOHNSON',
#                 'consent_datetime': datetime.today(),
#                 'dob': datetime.today() + relativedelta(years=-17),
#                 'identity_type': 'omang',
#                 'identity': '123456789',
#                 'confirm_identity': '123456789',
#                 'first_name': 'ERIK',
#                 'last_name': 'JOHN',
#                 'initials': 'JJ'}
#         subject_consent_form = SubjectConsentForm()
#         subject_consent_form.cleaned_data = data
#         self.assertRaisesRegexp(forms.ValidationError, 'initial does not match first name', subject_consent_form.clean)
#
#     def test_subject_consent_form11(self):
#         """report datetime must be between survey start and end datetime."""
#         self.household_member.eligible_subject = True
#         self.household_member.initials = 'EW'
#         data = {'household_member': self.household_member,
#                 'is_minor': 'Yes',
#                 'guardian_name': 'JOHNSON',
#                 'consent_datetime': datetime.today(),
#                 'dob': datetime.today() + relativedelta(years=-17),
#                 'identity_type': 'omang',
#                 'identity': '123456789',
#                 'confirm_identity': '123456789',
#                 'report_datetime': datetime(2013, 10, 10),
#                 'initials': 'DS'}
#         subject_consent_form = SubjectConsentForm()
#         subject_consent_form.cleaned_data = data
#         self.assertRaisesRegexp(
#             forms.ValidationError, 'Initials for household member record do not match', subject_consent_form.clean)
#
#     def test_subject_consent_form12(self):
#         """report datetime must be between survey start and end datetime."""
#         self.household_member.eligible_subject = True
#         self.household_member.initials = 'DS'
#         self.household_member.first_name = 'DAVID'
#         data = {'household_member': self.household_member,
#                 'is_minor': 'Yes',
#                 'guardian_name': 'JOHNSON',
#                 'consent_datetime': datetime.today(),
#                 'dob': datetime.today() + relativedelta(years=-17),
#                 'identity_type': 'omang',
#                 'identity': '123456789',
#                 'confirm_identity': '123456789',
#                 'report_datetime': datetime(2013, 10, 10),
#                 'initials': 'DS',
#                 'first_name': 'DON'}
#         subject_consent_form = SubjectConsentForm()
#         subject_consent_form.cleaned_data = data
#         self.assertRaisesRegexp(forms.ValidationError, 'First name does not match', subject_consent_form.clean)
#
#     def test_subject_consent_form13(self):
#         """report datetime must be between survey start and end datetime."""
#         self.household_member.eligible_subject = True
#         self.household_member.initials = 'DS'
#         self.household_member.first_name = 'DAVID'
#         self.household_member.gender = 'F'
#         data = {'household_member': self.household_member,
#                 'is_minor': 'Yes',
#                 'guardian_name': 'JOHNSON',
#                 'consent_datetime': datetime.today(),
#                 'dob': datetime.today() + relativedelta(years=-17),
#                 'identity_type': 'omang',
#                 'identity': '123456789',
#                 'confirm_identity': '123456789',
#                 'report_datetime': datetime(2013, 10, 10),
#                 'initials': 'DS',
#                 'first_name': 'DAVID',
#                 'gender': 'M'}
#         subject_consent_form = SubjectConsentForm()
#         subject_consent_form.cleaned_data = data
#         self.assertRaisesRegexp(forms.ValidationError, 'Gender does not match', subject_consent_form.clean)
