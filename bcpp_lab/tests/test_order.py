from datetime import datetime

from django.core.exceptions import ValidationError

from edc_constants.constants import NEW, POS, NEG, CLOSED, YES, NO
from bhp066.apps.bcpp_subject.constants import POC_VIRAL_LOAD, VIRAL_LOAD
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.core.bhp_variables.models import StudySite

from bhp066.apps.bcpp_lab.models import AliquotType, Panel
from bhp066.apps.bcpp_subject.models import HivCareAdherence
from bhp066.apps.bcpp_subject.models import HivResult

from bhp066.apps.bcpp_subject.tests.base_rule_group_test_setup import BaseRuleGroupTestSetup
from ..models import Aliquot, Receive, PreOrder, SubjectRequisition, AliquotProfile

from .factories import SubjectRequisitionFactory, ProcessingFactory


class TestOrder(BaseRuleGroupTestSetup):

    def hiv_result_poc(self, status, subject_visit, panel_label):
        """ Create HivResult for a particular survey"""
        aliquot_type = AliquotType.objects.all()[0]
        site = StudySite.objects.all()[0]
        microtube_panel = Panel.objects.get(name=panel_label)
        SubjectRequisitionFactory(
            subject_visit=subject_visit, panel=microtube_panel, aliquot_type=aliquot_type, site=site)

        self._hiv_result = HivResult.objects.create(
            subject_visit=subject_visit,
            hiv_result=status,
            report_datetime=datetime.today(),
            insufficient_vol=NO
        )
        return self._hiv_result

#     def test_create_negative_pre_order(self):
#         """ Create a single pre-order instance for HIV -ve participant"""
#         PreOrder.objects.all().delete()
#         self.subject_visit_male_T0 = self.baseline_subject_visit
#         self._hiv_result = self.hiv_result(NEG, self.subject_visit_male_T0)
#         self.assertEqual(PreOrder.objects.all().count(), 1)
#         self.assertEqual(PreOrder.objects.first().status, NEW)

#     def test_create_posetive_nopocvl_pre_order(self):
#         """ Create a single pre-order instance for HIV +ve participant who is on art"""
#         PreOrder.objects.all().delete()
#         self.subject_visit_male_T0 = self.baseline_subject_visit
#         self._hiv_result = self.hiv_result(POS, self.subject_visit_male_T0)
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=NO,
#             arv_evidence=NO,  # this is the rule field
#         )
#         self.assertEqual(PreOrder.objects.all().count(), 1)
#         self.assertEqual(PreOrder.objects.first().status, NEW)

    def test_create_posetive_withpocvl_pre_order(self):
        """ Create 2 pre-order instances for HIV +ve participant who is arv naive.
            One for normal viral load and the other for POC viral load"""
        self.subject_visit_male_T0 = self.baseline_subject_visit
        self._hiv_result = self.hiv_result(POS, self.subject_visit_male_T0)
        aliquot_type = AliquotType.objects.all()[0]
        viral_load_panel = Panel.objects.get(name='Viral Load')
        PreOrder.objects.all().delete()
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,
        )
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male_T0,
            panel=viral_load_panel,
            aliquot_type=aliquot_type,
            site=self.study_site
        )
        self.assertEqual(PreOrder.objects.all().count(), 1)
        self.assertEqual(PreOrder.objects.first().status, NEW)

    def test_create_posetive_withpocvl_pre_order_t1(self):
        """ Create 2 pre-order instances for HIV +ve participant who is arv naive.
            One for normal viral load and the other for POC viral load for T1"""
        self.subject_visit_male_T1 = self.annual_subject_visit_y2
        self._hiv_result = self.hiv_result(POS, self.subject_visit_male_T1)
        aliquot_type = AliquotType.objects.all()[0]
        viral_load_panel = Panel.objects.get(name='Viral Load')
        PreOrder.objects.all().delete()
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T1,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,
        )
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male_T1,
            panel=viral_load_panel,
            aliquot_type=aliquot_type,
            site=self.study_site
        )
        self.assertEqual(PreOrder.objects.all().count(), 1)
        self.assertEqual(PreOrder.objects.first().status, NEW)

#     def test_pre_order_with_aliquot(self):
#         """ Link pre order to aliquot"""
#         PreOrder.objects.all().delete()
#         self.subject_visit_male_T0 = self.baseline_subject_visit
#         self._hiv_result = self.hiv_result(NEG, self.subject_visit_male_T0)
#         self.assertEqual(PreOrder.objects.all().count(), 1)
#         self.assertEqual(PreOrder.objects.first().status, NEW)
#         requisition = SubjectRequisition.objects.get(panel__name='Microtube')
#         requisition.is_receive = True
#         requisition.is_receive_datetime = datetime.now()
#         requisition.save()
#         lab_profile = site_lab_profiles.get('SubjectRequisition')
#         lab_profile().receive(SubjectRequisition.objects.get(panel__name='Microtube'))
#         self.assertEqual(Receive.objects.all().count(), 1)
#         self.assertEqual(Aliquot.objects.all().count(), 1)
#         ProcessingFactory(aliquot=Aliquot.objects.first(), profile=AliquotProfile.objects.get(name='Microtube'))
#         pre_order = PreOrder.objects.first()
#         pre_order.aliquot_identifier = Aliquot.objects.get(aliquot_type__alpha_code='PL').aliquot_identifier
#         pre_order.save()
#         self.assertEqual(PreOrder.objects.first().status, CLOSED)
#         pre_order.aliquot_identifier = Aliquot.objects.get(aliquot_type__alpha_code='PL').aliquot_identifier + 'x'
#         with self.assertRaises(ValidationError):
#             pre_order.save()

#     def test_attempt_to_duplicate_pre_order_records(self):
#         """ Attempt to duplicate pre order records"""
#         PreOrder.objects.all().delete()
#         self.subject_visit_male_T0 = self.baseline_subject_visit
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=NO,
#             arv_evidence=NO,  # this is the rule field
#         )
#         self._hiv_result = self.hiv_result(POS, self.subject_visit_male_T0)
#         self.assertEqual(PreOrder.objects.all().count(), 1)
#         self.assertEqual(PreOrder.objects.first().status, NEW)
#         requisition = SubjectRequisition.objects.get(panel__name='Microtube')
#         # Attempt to duplicate pre order records
#         requisition.save()
#         self.assertEqual(PreOrder.objects.all().count(), 1)
#         self.assertEqual(PreOrder.objects.first().status, NEW)

    def test_attempt_to_link_multiple_preorder_to_same_aliquot(self):
        """ Attempt to link multiple pre order records to the same aliquot identifier"""
        PreOrder.objects.all().delete()
        self.subject_visit_male_T0 = self.baseline_subject_visit
        self._hiv_result = self.hiv_result(POS, self.subject_visit_male_T0)
        aliquot_type = AliquotType.objects.all()[0]
        viral_load_panel = Panel.objects.get(name='Viral Load')
        PreOrder.objects.all().delete()
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,
        )
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male_T0,
            panel=viral_load_panel,
            aliquot_type=aliquot_type,
            site=self.study_site
        )
        self.assertEqual(PreOrder.objects.all().count(), 1)
        self.assertEqual(PreOrder.objects.first().status, NEW)
        pre_order1 = PreOrder.objects.all()[0]

        # Process the primary aliquot
        lab_profile = site_lab_profiles.get('SubjectRequisition')
        lab_profile().receive(SubjectRequisition.objects.get(panel__name='Viral Load'))
        self.assertEqual(Receive.objects.all().count(), 1)
        self.assertEqual(Aliquot.objects.all().count(), 1)
        ProcessingFactory(aliquot=Aliquot.objects.first(), profile=AliquotProfile.objects.get(name='Viral Load'))

        pre_order1.aliquot_identifier = Aliquot.objects.filter(aliquot_type__alpha_code='PL').first().aliquot_identifier
        pre_order1.save()

#     def test_use_aliquot_that_belongs_to_subject(self):
#         """ Attempt to link multiple pre order records to the same aliquot identifier"""
#         PreOrder.objects.all().delete()
#         self.subject_visit_male_T0 = self.baseline_subject_visit
#         self._hiv_result = self.hiv_result(NEG, self.subject_visit_male_T0)
#         self.assertEqual(PreOrder.objects.all().count(), 1)
#         male_preorder = PreOrder.objects.all()[0]
#         self._hiv_result = self.hiv_result(NEG, self.subject_visit_female_T0)
#         self.assertEqual(PreOrder.objects.all().count(), 2)
# 
#         # Process the female's Aliquots.
#         lab_profile = site_lab_profiles.get('SubjectRequisition')
#         lab_profile().receive(SubjectRequisition.objects.get(subject_visit=self.subject_visit_female_T0, panel__name='Microtube'))
#         self.assertEqual(Receive.objects.all().count(), 1)
#         self.assertEqual(Aliquot.objects.all().count(), 1)
#         ProcessingFactory(aliquot=Aliquot.objects.first(), profile=AliquotProfile.objects.get(name='Microtube'))
# 
#         # Attempt to save the male_preorder using a female's aliquot
#         male_preorder.aliquot_identifier = Aliquot.objects.first().aliquot_identifier
# 
#         with self.assertRaises(ValidationError):
#             male_preorder.save()
