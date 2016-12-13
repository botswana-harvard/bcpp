# from datetime import date
#
# from django.core.exceptions import ValidationError
# from django.test import TestCase
# from django.db.models import get_model
#
# from edc.lab.lab_profile.classes import site_lab_profiles
# # from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
# # from edc_map.classes import Mapper, site_mappers
# # from edc_constants.constants import NOT_APPLICABLE
# from edc.subject.lab_tracker.classes import site_lab_tracker
# # from edc.subject.registration.models import RegisteredSubject
# from edc.subject.rule_groups.classes import site_rule_groups
# # from edc.core.bhp_variables.models import StudySite
# from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
# from edc.core.bhp_variables.models import StudySite
#
# from bhp066.apps.bcpp_lab.lab_profiles import BcppSubjectProfile
# from bhp066.apps.bcpp_subject.visit_schedule import BcppSubjectVisitSchedule
# from bhp066.apps.bcpp.app_configuration.classes import BcppAppConfiguration
# from bhp066.apps.bcpp_household.models import HouseholdStructure
# from bhp066.apps.bcpp_household.tests.factories import PlotFactory
# from bhp066.apps.member.tests.factories import HouseholdMemberFactory
# # from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory
# # from bhp066.apps.bcpp_subject.models import SubjectVisit
# from bhp066.apps.bcpp_subject.tests.factories import SubjectVisitFactory
# from bhp066.apps.bcpp.choices import (
#     YES_NO_DWTA, ALCOHOL_SEX, FREQ_IN_YEAR, SEXDAYS_CHOICE, LASTSEX_CHOICE, YES_NO_UNSURE,
#     AGE_RANGES, FIRSTRELATIONSHIP_CHOICE, YES_NO_UNSURE_DWTA, FIRSTDISCLOSE_CHOICE, FIRSTCONDOMFREQ_CHOICE)
# #
# # from bhp066.apps.bcpp_subject.forms import SexualBehaviourForm, MonthsRecentPartnerForm
# from bhp066.apps.bcpp_household.tests.factories import RepresentativeEligibilityFactory
#
# from .factories import (SubjectConsentFactory, SubjectVisitFactory)
#
#
# class TestSexualBehaviourForm(TestCase):
#     def setUp(self):
#         try:
#             site_lab_profiles.register(BcppSubjectProfile())
#         except AlreadyRegisteredLabProfile:
#             pass
#         BcppAppConfiguration().prepare()
#         site_lab_tracker.autodiscover()
#         BcppSubjectVisitSchedule().build()
#         site_rule_groups.autodiscover()
#
# #         StudySiteFactory()
# #         self.survey = SurveyFactory()
#         self.study_site = StudySite.objects.get(site_code='01')
#         self.plot = PlotFactory(community='test_community', household_count=1, status='residential_habitable')
#         self.household_structure = HouseholdStructure.objects.filter(household__plot=self.plot).first()
#
#         RepresentativeEligibilityFactory(household_structure=self.household_structure)
#
#         self.household_member = HouseholdMemberFactory(household_structure=self.household_structure)
#
#         SubjectConsentFactory(
#             household_member=self.household_member, confirm_identity='101129811', identity='101129811',
#             study_site=self.study_site, gender='M',
#             dob=date(1990, 1, 1), first_name='ERIK',
#             initials='EW')
#
#         self.subject_visit = SubjectVisitFactory(household_member=self.household_member)
#         self.data = {'ever_sex': YES_NO_DWTA[2][0], 'lifetime_sex_partners': 0, 'last_year_partners': 0,
#                      'more_sex': YES_NO_DWTA[2][0], 'condom': YES_NO_DWTA[2][0], 'alcohol_sex': ALCOHOL_SEX[0][0]}
#
# #     def setUp(self):
# #         StudySpecificFactory()
#
#     def test_subject_visit(self):
#         """
#         Tests whether the subject visit has been created.
#         """
#         self.assertEqual(SubjectVisit.objects.filter(household_member=self.household_member).count(), 1)
#
#     def test_ever_sex_if_no(self):
#         """ """
#         self.data['more_sex'] = YES_NO_DWTA[1][0]
#         sexual_behaviour_form = SexualBehaviourForm(data=self.data)
#         self.assertRaises(ValidationError, sexual_behaviour_form.clean())
#
#     def test_is_ecc_on_recent_partner(self):
#         """  (Recent Partner 12 months, Second Partner 12 months, Third Partner 12 months) If outside community or
#               farm outside this community ask: Does this sexual partner live in any of the following communities?
#               if response is a ecc community then derived value should assign ecc
#         """
#         PartnerResidency = get_model('bcpp_list', 'partnerresidency')
#         first_partner_communities = [PartnerResidency.objects.get(name='In this community')]
#         data = {'subject_visit': self.subject_visit,
#                 'first_partner_live': first_partner_communities,
#                 'sex_partner_community': 'ranaka',
#                 'past_year_sex_freq': FREQ_IN_YEAR[1][0],
#                 'third_last_sex': SEXDAYS_CHOICE[0][0],
#                 'third_last_sex_calc': 2,
#                 'first_first_sex': LASTSEX_CHOICE[0][0],
#                 'first_first_sex_calc': 0,
#                 'first_sex_current': YES_NO_DWTA[0][0],
#                 'first_relationship': FIRSTRELATIONSHIP_CHOICE[1][0],
#                 'first_exchange': AGE_RANGES[1][0],
#                 'concurrent': YES_NO_DWTA[1][0],
#                 'goods_exchange': YES_NO_DWTA[1][0],
#                 'first_sex_freq': 3,
#                 'partner_hiv_test': YES_NO_UNSURE_DWTA[1][0],
#                 'first_partner_hiv': YES_NO_UNSURE[1][0],
#                 'first_disclose': FIRSTDISCLOSE_CHOICE[0][0],
#                 'first_condom_freq': FIRSTCONDOMFREQ_CHOICE[0][0],
#                 'first_partner_cp': YES_NO_UNSURE[2][1]
#                 }
#         recent_partner_form = MonthsRecentPartnerForm()
#         recent_partner_form.cleaned_data = data
#         recent_partner_form.save()
#         self.assertEqual(recent_partner_form.instance.is_ecc_or_cpc(), 'ECC')
#
#     def test_is_cpc_on_recent_partner(self):
#         """  (Recent Partner 12 months, Second Partner 12 months, Third Partner 12 months) If outside community or
#           farm outside this community ask: Does this sexual partner live in any of the following communities?
#           if response is a cpc community then derived value should assign cpc"""
#         PartnerResidency = get_model('bcpp_list', 'partnerresidency')
#         first_partner_communities = [PartnerResidency.objects.get(
#             name__in=['In this community', 'Farm within this community', 'Cattle post within this community'])]
#         data = {'subject_visit': self.subject_visit,
#                 'first_partner_live': first_partner_communities,
#                 'sex_partner_community': 'digawana',
#                 'past_year_sex_freq': FREQ_IN_YEAR[1][0],
#                 'third_last_sex': SEXDAYS_CHOICE[0][0],
#                 'third_last_sex_calc': 2,
#                 'first_first_sex': LASTSEX_CHOICE[0][0],
#                 'first_first_sex_calc': 0,
#                 'first_sex_current': YES_NO_DWTA[0][0],
#                 'first_relationship': FIRSTRELATIONSHIP_CHOICE[1][0],
#                 'first_exchange': AGE_RANGES[1][0],
#                 'concurrent': YES_NO_DWTA[1][0],
#                 'goods_exchange': YES_NO_DWTA[1][0],
#                 'first_sex_freq': 3,
#                 'partner_hiv_test': YES_NO_UNSURE_DWTA[1][0],
#                 'first_partner_hiv': YES_NO_UNSURE[1][0],
#                 'first_disclose': FIRSTDISCLOSE_CHOICE[0][0],
#                 'first_condom_freq': FIRSTCONDOMFREQ_CHOICE[0][0],
#                 'first_partner_cp': YES_NO_UNSURE[2][1]
#                 }
#         recent_partner_form = MonthsRecentPartnerForm()
#         recent_partner_form.cleaned_data = data
#         recent_partner_form.save()
#         self.assertEqual(recent_partner_form.instance.first_partner_arm, 'CPC')
#
#     def test_derived_on_na(self):
#         """  (Recent Partner 12 months, Second Partner 12 months, Third Partner 12 months) If outside community or
#               farm outside this community ask: Does this sexual partner live in any of the following communities?
#               if response is a other community then derived value should assign NOT_APPLICABLE
#         """
#         PartnerResidency = get_model('bcpp_list', 'partnerresidency')
#         first_partner_communities = [PartnerResidency.objects.get(
#             name__in=['In this community']), PartnerResidency.objects.get(name='Outside community')]
#         data = {'subject_visit': self.subject_visit,
#                 'first_partner_live': first_partner_communities,
#                 'sex_partner_community': NOT_APPLICABLE,
#                 'past_year_sex_freq': FREQ_IN_YEAR[1][0],
#                 'third_last_sex': SEXDAYS_CHOICE[0][0],
#                 'third_last_sex_calc': 2,
#                 'first_first_sex': LASTSEX_CHOICE[0][0],
#                 'first_first_sex_calc': 0,
#                 'first_sex_current': YES_NO_DWTA[0][0],
#                 'first_relationship': FIRSTRELATIONSHIP_CHOICE[1][0],
#                 'first_exchange': AGE_RANGES[1][0],
#                 'concurrent': YES_NO_DWTA[1][0],
#                 'goods_exchange': YES_NO_DWTA[1][0],
#                 'first_sex_freq': 3,
#                 'partner_hiv_test': YES_NO_UNSURE_DWTA[1][0],
#                 'first_partner_hiv': YES_NO_UNSURE[1][0],
#                 'first_disclose': FIRSTDISCLOSE_CHOICE[0][0],
#                 'first_condom_freq': FIRSTCONDOMFREQ_CHOICE[0][0],
#                 'first_partner_cp': YES_NO_UNSURE[2][1]
#                 }
#         recent_partner_form = MonthsRecentPartnerForm()
#         recent_partner_form.cleaned_data = data
#         recent_partner_form.save()
#         self.assertEqual(recent_partner_form.instance.first_partner_arm, NOT_APPLICABLE)
#
#     def test_derived_on_other(self):
#         """  (Recent Partner 12 months, Second Partner 12 months, Third Partner 12 months) If outside community or
#               farm outside this community ask: Does this sexual partner live in any of the following communities?
#               if response is a other community then derived value should assign OTHER.
#         """
#         PartnerResidency = get_model('bcpp_list', 'partnerresidency')
#         first_partner_communities = [PartnerResidency.objects.get(
#             name='In this community'), PartnerResidency.objects.get(name='Outside community')]
#         data = {'subject_visit': self.subject_visit,
#                 'first_partner_live': first_partner_communities,
#                 'sex_partner_community': 'OTHER',
#                 'past_year_sex_freq': FREQ_IN_YEAR[1][0],
#                 'third_last_sex': SEXDAYS_CHOICE[0][0],
#                 'third_last_sex_calc': 2,
#                 'first_first_sex': LASTSEX_CHOICE[0][0],
#                 'first_first_sex_calc': 0,
#                 'first_sex_current': YES_NO_DWTA[0][0],
#                 'first_relationship': FIRSTRELATIONSHIP_CHOICE[1][0],
#                 'first_exchange': AGE_RANGES[1][0],
#                 'concurrent': YES_NO_DWTA[1][0],
#                 'goods_exchange': YES_NO_DWTA[1][0],
#                 'first_sex_freq': 3,
#                 'partner_hiv_test': YES_NO_UNSURE_DWTA[1][0],
#                 'first_partner_hiv': YES_NO_UNSURE[1][0],
#                 'first_disclose': FIRSTDISCLOSE_CHOICE[0][0],
#                 'first_condom_freq': FIRSTCONDOMFREQ_CHOICE[0][0],
#                 'first_partner_cp': YES_NO_UNSURE[2][1]
#                 }
#         recent_partner_form = MonthsRecentPartnerForm()
#         recent_partner_form.cleaned_data = data
#         recent_partner_form.save()
#         self.assertEqual(recent_partner_form.instance.first_partner_arm, 'OTHER')
#
#     def test_derived_on_blank(self):
#         """  (Recent Partner 12 months, Second Partner 12 months, Third Partner 12 months) If outside community or
#               farm outside this community ask: Does this sexual partner live in any of the following communities?
#               if response is a other community then derived value should assign blank
#         """
#         PartnerResidency = get_model('bcpp_list', 'partnerresidency')
#         first_partner_communities = [PartnerResidency.objects.get(
#             name='In this community'), PartnerResidency.objects.get(name='Outside community')]
#         data = {'subject_visit': self.subject_visit,
#                 'first_partner_live': first_partner_communities,
#                 'sex_partner_community': '',
#                 'past_year_sex_freq': FREQ_IN_YEAR[1][0],
#                 'third_last_sex': SEXDAYS_CHOICE[0][0],
#                 'third_last_sex_calc': 2,
#                 'first_first_sex': LASTSEX_CHOICE[0][0],
#                 'first_first_sex_calc': 0,
#                 'first_sex_current': YES_NO_DWTA[0][0],
#                 'first_relationship': FIRSTRELATIONSHIP_CHOICE[1][0],
#                 'first_exchange': AGE_RANGES[1][0],
#                 'concurrent': YES_NO_DWTA[1][0],
#                 'goods_exchange': YES_NO_DWTA[1][0],
#                 'first_sex_freq': 3,
#                 'partner_hiv_test': YES_NO_UNSURE_DWTA[1][0],
#                 'first_partner_hiv': YES_NO_UNSURE[1][0],
#                 'first_disclose': FIRSTDISCLOSE_CHOICE[0][0],
#                 'first_condom_freq': FIRSTCONDOMFREQ_CHOICE[0][0],
#                 'first_partner_cp': YES_NO_UNSURE[2][1]
#                 }
#         recent_partner_form = MonthsRecentPartnerForm()
#         recent_partner_form.cleaned_data = data
#         recent_partner_form.save()
#         self.assertEqual(recent_partner_form.instance.first_partner_arm, '')
