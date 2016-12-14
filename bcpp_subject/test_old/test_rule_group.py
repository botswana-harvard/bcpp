from datetime import datetime, timedelta

from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc_constants.constants import NEW, NOT_REQUIRED, KEYED, REQUIRED, POS, NEG, YES, NO
from edc_quota.client.models import Quota

from bhp066.apps.bcpp_lab.tests.factories import SubjectRequisitionFactory
from bhp066.apps.bcpp_lab.models import Panel, AliquotType

from bhp066.apps.bcpp_subject.models import (
    HivCareAdherence, HivTestingHistory, HivTestReview, ElisaHivResult,
    Circumcision, Circumcised, HicEnrollment, SubjectLocator, HivResult)

from .factories import (SubjectVisitFactory, CircumcisionFactory, ResidencyMobilityFactory, HivTestingHistoryFactory,
                        SubjectLocatorFactory)
from .base_rule_group_test_setup import BaseRuleGroupTestSetup


class TestRuleGroup(BaseRuleGroupTestSetup):

    def test_hiv_car_adherence_and_pima1(self):
        """ HIV Positive took arv in the past but now defaulting, Should NOT offer POC CD4.

        Models:
            * HivCareAdherence
            * HivResult
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_car_adherence_options = {}
        hiv_car_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male_T0.appointment)
        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T0.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **hiv_car_adherence_options).count(), 1)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=YES,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )
        # said they have taken ARV so not required
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

    def test_hiv_car_adherence_and_pima2(self):
        """If POS and on arv and have doc evidence, Pima not required, not a defaulter.

        Models:
            * HivCareAdherence
            * HivResult
        """

        hiv_car_adherence_options = {}
        hiv_car_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_female_T0.appointment)
        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_female_T0.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_car_adherence_options).count(), 1)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_female_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=YES,
            arv_evidence=YES,
        )

        # on art so no need for CD4
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

    def test_hiv_car_adherence_and_pima3(self):
        """If POS and on arv but do not have doc evidence, Pima required.

        Models:
            * HivCareAdherence
            * HivResult
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_car_adherence_options = {}
        hiv_car_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male_T0.appointment)
        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T0.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_car_adherence_options).count(), 1)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=YES,
            arv_evidence=NO,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

    def test_newly_pos_and_not_art_bhs(self):
        """Newly HIV Positive not on ART at T0, Should offer POC CD4.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T0.appointment)

        self._hiv_result = self.hiv_result(POS, self.subject_visit_male_T0)

        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)

    def test_not_known_pos_runs_hiv_and_cd4(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male_T0.appointment)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T0.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male_T0.appointment)

        # add HivTestReview,
        hiv_test_review = HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=NEG,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

        hiv_test_review.recorded_hiv_result = 'IND'
        hiv_test_review.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

        hiv_test_review.recorded_hiv_result = 'UNK'
        hiv_test_review.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

    def test_known_pos_completes_hiv_care_adherence(self):
        """If known POS (not including today's test), requires hiv_care_adherence."""
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male_T0.appointment)

        hiv_care_adherence_options = {}
        hiv_care_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male_T0.appointment)

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_care_adherence_options).count(), 1)

    def test_known_neg_does_not_complete_hiv_care_adherence(self):
        """If known POS (not including today's test), requires hiv_care_adherence."""
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_test_history_options = {}
        hiv_test_history_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestinghistory',
            appointment=self.subject_visit_male_T0.appointment)

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male_T0.appointment)

        hiv_care_adherence_options = {}
        hiv_care_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male_T0.appointment)

        # add HivTestHistory,
        hiv_testing_history = HivTestingHistoryFactory(subject_visit=self.subject_visit_male_T0)
        hiv_testing_history.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_history_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_test_review_options).count(), 1)
        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=NEG,
        )
        # hiv_care_adherence.save()

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_care_adherence_options).count(), 1)

    def test_known_neg_requires_hiv_test_today(self):
        """If previous result is NEG, need to test today (HivResult).

        See rule_groups.ReviewNotPositiveRuleGroup
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male_T0.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male_T0.appointment)

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=NEG,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)

    def test_known_pos_does_not_require_hiv_test_today(self):
        """If previous result is POS, do not need to test today (HivResult).

        See rule_groups.ReviewNotPositiveRuleGroup
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male_T0.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male_T0.appointment)

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_options).count(), 1)

    def test_known_pos_stigma_forms(self):
        """If known posetive, test stigma forms
        """
        self.subject_visit_female_T0.delete()
        self.subject_visit_female_T0 = SubjectVisitFactory(appointment=self.appointment_female_T0, household_member=self.household_member_female_T0)
        self.check_male_registered_subject_rule_groups(self.subject_visit_female_T0)

        hiv_test_history_options = {}
        hiv_test_history_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestinghistory',
            appointment=self.subject_visit_female_T0.appointment)

        stigma_options = {}
        stigma_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='stigma',
            appointment=self.subject_visit_female_T0.appointment)

        stigmaopinion_options = {}
        stigmaopinion_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='stigmaopinion',
            appointment=self.subject_visit_female_T0.appointment)

        hiv_testing_history = HivTestingHistoryFactory(subject_visit=self.subject_visit_female_T0)
        hiv_testing_history.save()

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_history_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **stigma_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **stigmaopinion_options).count(), 1)

    def test_hiv_tested_forms(self):
        """If known posetive, test hivtested forms
        """
        self.subject_visit_female_T0.delete()
        self.subject_visit_female_T0 = SubjectVisitFactory(appointment=self.appointment_female_T0, household_member=self.household_member_female_T0)
        self.check_male_registered_subject_rule_groups(self.subject_visit_female_T0)

        hiv_test_history_options = {}
        hiv_test_history_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestinghistory',
            appointment=self.subject_visit_female_T0.appointment)

        hiv_untested_options = {}
        hiv_untested_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivuntested',
            appointment=self.subject_visit_female_T0.appointment)

        hiv_tested_options = {}
        hiv_tested_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtested',
            appointment=self.subject_visit_female_T0.appointment)

        hiv_testing_history = HivTestingHistoryFactory(subject_visit=self.subject_visit_female_T0)
        hiv_testing_history.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_history_options).count(), 1),
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_tested_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_untested_options).count(), 1)

        hiv_testing_history.has_tested = NO
        hiv_testing_history.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_untested_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_tested_options).count(), 1)

    def test_cancer_hearattack_tb_forms(self):
        """Medical diagnoses forms
        """
        self.subject_visit_female_T0.delete()
        self.subject_visit_female_T0 = SubjectVisitFactory(appointment=self.appointment_female_T0, household_member=self.household_member_female_T0)
        self.check_male_registered_subject_rule_groups(self.subject_visit_female_T0)

        heartattack_options = {}
        heartattack_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='heartattack',
            appointment=self.subject_visit_female_T0.appointment)

        cancer_options = {}
        cancer_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='cancer',
            appointment=self.subject_visit_female_T0.appointment)

        tbsymptoms_options = {}
        tbsymptoms_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='tbsymptoms',
            appointment=self.subject_visit_female_T0.appointment)

        medicaldiagnoses_options = {}
        medicaldiagnoses_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='medicaldiagnoses',
            appointment=self.subject_visit_female_T0.appointment)

    def test_known_pos_on_art_no_doc_requires_cd4_only(self):
        """If previous result is POS on art but no evidence, need to run CD4 (Pima).

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male_T0.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male_T0.appointment)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T0.appointment)

        hiv_care_adherence_options = {}
        hiv_care_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male_T0.appointment)

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_care_adherence_options).count(), 1)

        # add HivCareAdherence,
        care_adherance = HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=YES,
            arv_evidence=NO,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

        care_adherance.on_arv = NO
        care_adherance.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **pima_options).count(), 1)

    def test_hiv_care_adherance_for_verbal_posetive_only(self):
        """HivCareAdharance form should be made available any verbal positive,
            not considering availability or lack thereof documentation.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male_T0,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=NO,
            verbal_hiv_result=POS,
            other_record=NO
        )

        hiv_care_adherence_options = {}
        hiv_care_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male_T0.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(
            entry_status=NEW, **hiv_care_adherence_options).count(), 1)

    def test_known_pos_on_art_with_doc_requires_cd4_only(self):
        """If previous result is POS on art with doc evidence, do not run HIV or CD4.

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male_T0.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male_T0.appointment)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T0.appointment)

        hiv_care_adherence_options = {}
        hiv_care_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male_T0.appointment)

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_care_adherence_options).count(), 1)

        # add HivCareAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=YES,
            arv_evidence=YES,  # this is the rule field
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

    def test_known_pos_no_art_but_has_doc_requires_cd4_only(self):
        """If previous result is POS on art but no evidence, need to run CD4 (Pima).

        This is a defaulter

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male_T0.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male_T0.appointment)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T0.appointment)

        hiv_care_adherence_options = {}
        hiv_care_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male_T0.appointment)

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_care_adherence_options).count(), 1)

        # add HivCareAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=YES,  # this is the rule field
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **hiv_care_adherence_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)

    def test_elisaresult_behaves_like_todayhivresult(self):
        """when an elisa result is keyed in, a +ve result should result in RBD and VL
            being REQUIRED just like Today's HivResult
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male_T0.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male_T0.appointment)

        elisa_hiv_result_options = {}
        elisa_hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='elisahivresult',
            appointment=self.subject_visit_male_T0.appointment)

        research_blood_draw_options = {}
        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male_T0.appointment)

        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male_T0.appointment)

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=NEG,
        )
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **elisa_hiv_result_options).count(), 1)

        self._hiv_result = self.hiv_result('IND', self.subject_visit_male_T0)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **elisa_hiv_result_options).count(), 1)

        elisa_panel = Panel.objects.get(name='ELISA')
        aliquot_type = AliquotType.objects.all()[0]
        site = self.study_site
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male_T0, panel=elisa_panel, aliquot_type=aliquot_type, site=site)
        ElisaHivResult.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_result=POS,
            hiv_result_datetime=datetime.today(),
        )
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **elisa_hiv_result_options).count(), 1)

        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)

    def test_normal_circumsition_in_y1(self):

        self.subject_visit_male_T0 = self.baseline_subject_visit

        circumsition_options = {}
        circumsition_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='circumcision',
            appointment=self.subject_visit_male_T0.appointment)

        circumcised_options = {}
        circumcised_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='circumcised',
            appointment=self.subject_visit_male_T0.appointment)

        uncircumcised_options = {}
        uncircumcised_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='uncircumcised',
            appointment=self.subject_visit_male_T0.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **circumsition_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **uncircumcised_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **circumcised_options).count(), 1)

        circumcition = CircumcisionFactory(subject_visit=self.subject_visit_male_T0, circumcised=YES)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **circumsition_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **uncircumcised_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **circumcised_options).count(), 1)

        self._hiv_result = self.hiv_result(NEG, self.subject_visit_male_T0)

        # Enforce that entering an HivResult does not affect Circumcition Meta Data.
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **circumsition_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **uncircumcised_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **circumcised_options).count(), 1)

        circumcition.circumcised = NO
        circumcition.save()

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **circumsition_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **uncircumcised_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **circumcised_options).count(), 1)

        circumcition.circumcised = 'Not Sure'
        circumcition.save()

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **circumsition_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **uncircumcised_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **circumcised_options).count(), 1)

    def test_no_circumsition_in_y2(self):
        self.subject_visit_male_T0 = self.baseline_subject_visit

        circumsition_options = {}
        circumsition_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='circumcision',
            appointment=self.subject_visit_male.appointment)

        circumcised_options = {}
        circumcised_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='circumcised',
            appointment=self.subject_visit_male.appointment)

        uncircumcised_options = {}
        uncircumcised_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='uncircumcised',
            appointment=self.subject_visit_male.appointment)

        Circumcision.objects.create(
            subject_visit=self.subject_visit_male_T0,
            circumcised=YES
        )

        Circumcised.objects.create(
            subject_visit=self.subject_visit_male_T0,
            where_circ='Lobatse',
            why_circ='not_sure'
        )

        self.subject_visit_male.delete()
        # Create circumsided dude's year 1 visit
        self.subject_visit_male = SubjectVisitFactory(appointment=self.appointment_male, household_member=self.household_member_male)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **circumsition_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **circumcised_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **uncircumcised_options).count(), 1)

    def test_pos_in_y1_no_hiv_forms(self):
        self.subject_visit_male_T0 = self.baseline_subject_visit

        self._hiv_result = self.hiv_result(POS, self.subject_visit_male_T0)

        self.subject_visit_male = self.annual_subject_visit_y2

        hiv_test_review_options = {}
        hiv_test_review_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestreview',
            appointment=self.subject_visit_male.appointment)

        hiv_tested_options = {}
        hiv_tested_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtested',
            appointment=self.subject_visit_male.appointment)

        hiv_testing_history_options = {}
        hiv_testing_history_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivtestinghistory',
            appointment=self.subject_visit_male.appointment)

        hiv_result_documentation_options = {}
        hiv_result_documentation_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresultdocumentation',
            appointment=self.subject_visit_male.appointment)

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male.appointment)

        microtube_options = {}
        microtube_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Microtube',
            appointment=self.subject_visit_male.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_test_review_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_tested_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_testing_history_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_documentation_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **microtube_options).count(), 1)

    def test_hic_filled_in_y1_notrequired_in_annual(self):
        self.subject_visit_male_T0 = self.baseline_subject_visit

        SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
                              subject_visit=self.subject_visit_male_T0)

        ResidencyMobilityFactory(subject_visit=self.subject_visit_male_T0)

        self.hiv_result(NEG, self.subject_visit_male_T0)

        HicEnrollment.objects.create(
            subject_visit=self.subject_visit_male_T0,
            report_datetime=datetime.today(),
            hic_permission=YES)

        subject_visit_male = self.annual_subject_visit_y2

        self.hiv_result(NEG, subject_visit_male)

        hic_enrollment_options = {}
        hic_enrollment_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hicenrollment',
            appointment=subject_visit_male.appointment)

        microtube_options = {}
        microtube_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Microtube',
            appointment=subject_visit_male.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED,
                                                               **hic_enrollment_options).count(), 1)

        subject_visit_male_T2 = self.annual_subject_visit_y3

        self.hiv_result(NEG, subject_visit_male_T2)

        hic_enrollment_options.update(appointment=subject_visit_male_T2.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED,
                                                               **hic_enrollment_options).count(), 1)

    def test_microtube_always_required_for_hic_without_pos_hivresult(self):
        """ Tests that an HIC enrollee who sero-converted to POS status, but the POS result not tested by BHP,
            will be tested by BHP at next visit. """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
                              subject_visit=self.subject_visit_male_T0)

        self.hiv_result(NEG, self.subject_visit_male_T0)

        ResidencyMobilityFactory(subject_visit=self.subject_visit_male_T0)

        self.assertEqual(SubjectLocator.objects.filter(subject_visit=self.subject_visit_male_T0).count(), 1)
        HicEnrollment.objects.create(
            subject_visit=self.subject_visit_male_T0,
            report_datetime=datetime.today(),
            hic_permission=YES)

        self.subject_visit_male = self.annual_subject_visit_y2

        microtube_options = {}
        microtube_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Microtube',
            appointment=self.subject_visit_male.appointment)
        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male.appointment)

        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NEW, **microtube_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)
        # Make participant known positive in year 2, microtube and hiv result should remain required
        # NOTE: We are using HivTestingHistory and HivTestReview to create the POS status because the participant
        # was not tested by BHP, they became POS after our last visit with them.
        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NEW, **microtube_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NEW, **hiv_result_options).count(), 1)

    def test_microtube_not_required_for_hic_with_pos_hivresult(self):
        """ Tests that an HIC enrollee who sero-converted to POS status, tested by BHP, will not be tested
            again in next visit."""
        self.subject_visit_male_T0 = self.baseline_subject_visit

        SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
                              subject_visit=self.subject_visit_male_T0)

        self.hiv_result(NEG, self.subject_visit_male_T0)

        ResidencyMobilityFactory(subject_visit=self.subject_visit_male_T0)

        self.assertEqual(SubjectLocator.objects.filter(subject_visit=self.subject_visit_male_T0).count(), 1)
        HicEnrollment.objects.create(
            subject_visit=self.subject_visit_male_T0,
            report_datetime=datetime.today(),
            hic_permission=YES)

        self.subject_visit_male = self.annual_subject_visit_y2
        # Make participant known positive in year 2, tested by BHP. That means hey have an HivResult record with POS
        # NOTE: We are using HivResult to indicate that the HIV POS result was tested by BHP.
        self.hiv_result(POS, self.subject_visit_male)
        # We are now in year 3 in which the participant is a known POS.
        self.subject_visit_male_T2 = self.annual_subject_visit_y3

        microtube_options = {}
        microtube_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Microtube',
            appointment=self.subject_visit_male_T2.appointment)
        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male_T2.appointment)

        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **microtube_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED,
                                                               **hiv_result_options).count(), 1)

    def test_hiv_pos_requisitions_y2(self):
        """ HIV Negative and in HIC at T0 and Tests Positive during home visits at T1 and is Not on ART at T1.
            Sero Converter, Should offer POC CD4, RBD and VL.
        """

        self.subject_visit_male_T0 = self.baseline_subject_visit

        SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
                              subject_visit=self.subject_visit_male_T0)

        ResidencyMobilityFactory(subject_visit=self.subject_visit_male_T0)

        self.hiv_result(NEG, self.subject_visit_male_T0)

        HicEnrollment.objects.create(
            subject_visit=self.subject_visit_male_T0,
            report_datetime=datetime.today(),
            hic_permission=YES)

        self.subject_visit_male = self.annual_subject_visit_y2

        self.hiv_result(POS, self.subject_visit_male)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male.appointment)

        research_blood_draw_options = {}
        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)

    def test_Known_hiv_pos_y2_not_hic_require_no_testing(self):
        self.subject_visit_male_T0 = self.baseline_subject_visit

        # They were NEG in year 1
        self.hiv_result(NEG, self.subject_visit_male_T0)

        self.subject_visit_male = self.annual_subject_visit_y2

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male.appointment)

        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_options).count(), 1)

        self.subject_visit_male_T2 = self.annual_subject_visit_y3
        hiv_result_options.update(appointment=self.subject_visit_male_T2.appointment)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_options).count(), 1)

    def test_Known_hiv_pos_y3_not_hic_require_no_testing_missed_y2(self):
        self.subject_visit_male_T0 = self.baseline_subject_visit

        # Known POS in T0
        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male_T0,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        # Misses T1, and is seen again at T2. They should not be Tested.
        self.subject_visit_male_T2 = self.annual_subject_visit_y3

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male_T2.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_options).count(), 1)

    def test_Known_hiv_pos_y1_require_no_testing(self):
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_result_options = {}
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male_T0.appointment)

        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male_T0,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hiv_result_options).count(), 1)

#     def hiv_pos_and_art_naive_pimavl_bhs(self):
#         """HIV Positive not on ART at T0, Should offer POC VL at BHS"""
#         self.subject_visit_male_T0 = self.baseline_subject_visit
#
#         pima_vl_options = {}
#         pima_vl_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pimavl',
#             appointment=self.subject_visit_male_T0.appointment)
#
#         HivTestingHistory.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             has_tested=YES,
#             when_hiv_test='1 to 5 months ago',
#             has_record=YES,
#             verbal_hiv_result=POS,
#             other_record=NO
#         )
#
#         HivTestReview.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             hiv_test_date=datetime.today() - timedelta(days=50),
#             recorded_hiv_result=POS,
#         )
#         # known pos
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male_T0,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=NO,
#             arv_evidence=NO,  # this is the rule field
#         )
#
# #         quota = Quota.objects.create(
# #             app_label='bcpp_subject',
# #             model_name='PimaVl',
# #             target=2,
# #             expires_datetime=datetime.now() + timedelta(days=1)
# #     )
# #         self.assertEqual(Quota.objects.all().count(), 1)
# #         PimaVlFactory(subject_visit=self.subject_visit_male_T0)
# #
# #         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=KEYED, **pima_vl_options).count(), 1)
#
#     def test_hiv_pos_and_art_naive_pimavl_ahs(self):
#         """HIV Positive not on ART at T0, Should offer POC VL at BHS
#            HIV Positive not on ART at T1 Should again offer POC VL AHS"""
#
#         # Takes care of T0 environment
#         self.hiv_pos_and_art_naive_pimavl_bhs()
#
#         self.subject_visit_male = self.annual_subject_visit_y2
#
#         pima_vl_options = {}
#         pima_vl_options.update(
#             entry__app_label='bcpp_subject',
#             entry__model_name='pimavl',
#             appointment=self.subject_visit_male.appointment)
#
#         HivTestingHistory.objects.create(
#             subject_visit=self.subject_visit_male,
#             has_tested=YES,
#             when_hiv_test='1 to 5 months ago',
#             has_record=YES,
#             verbal_hiv_result=POS,
#             other_record=NO
#         )
#
#         HivTestReview.objects.create(
#             subject_visit=self.subject_visit_male,
#             hiv_test_date=datetime.today() - timedelta(days=50),
#             recorded_hiv_result=POS,
#         )
#
#         HivCareAdherence.objects.create(
#             subject_visit=self.subject_visit_male,
#             first_positive=None,
#             medical_care=NO,
#             ever_recommended_arv=NO,
#             ever_taken_arv=NO,
#             on_arv=NO,
#             arv_evidence=NO,  # this is the rule field
#         )
#
#         self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_vl_options).count(), 1)

    def test_hic_enrolled_at_bhs(self):
        """ If there is an hic record at bhs then at ahs inspect the record then check for hic status if not enrolled then Hic_enrollment
            should be filled otherwise should not be filled.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        ResidencyMobilityFactory(subject_visit=self.subject_visit_male_T0)

        hic_enrollment_options = {}
        hic_enrollment_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hicenrollment',
            appointment=self.subject_visit_male_T0.appointment)

        SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
                              subject_visit=self.subject_visit_male_T0)

        self.hiv_result(NEG, self.subject_visit_male_T0)

        HicEnrollment.objects.create(
            subject_visit=self.subject_visit_male_T0,
            report_datetime=datetime.today(),
            hic_permission=YES)

        self.subject_visit_male = self.annual_subject_visit_y2

        hic_enrollment_options.update(appointment=self.subject_visit_male.appointment)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hic_enrollment_options).count(), 1)

        self.subject_visit_male_T2 = self.annual_subject_visit_y3

        hic_enrollment_options.update(appointment=self.subject_visit_male_T2.appointment)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **hic_enrollment_options).count(), 1)

    def test_hic_not_enrolled_at_bhs(self):
        """ If there is an hic record inspect the record then check for hic status if not enrolled then Hic_enrollment
            should be offered again at T1.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
                              subject_visit=self.subject_visit_male_T0)

        ResidencyMobilityFactory(subject_visit=self.subject_visit_male_T0)

        hic_enrollment_options = {}
        hic_enrollment_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hicenrollment',
            appointment=self.subject_visit_male_T0.appointment)

        self.hiv_result(NEG, self.subject_visit_male_T0)

        HicEnrollment.objects.create(
            subject_visit=self.subject_visit_male_T0,
            report_datetime=datetime.today(),
            hic_permission=NO)

        self.subject_visit_male = self.annual_subject_visit_y2

        hic_enrollment_options.update(appointment=self.subject_visit_male.appointment)

        self.hiv_result(NEG, self.subject_visit_male)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **hic_enrollment_options).count(), 1)

    def test_hiv_pos_nd_art_naive_at_ahs_new_erollee(self):
        """New enrollees at T0 (i.e doing BHS procedures) who are HIV-positive and ART naive, then PIMA required.
        """
        self.subject_visit_male = self.annual_subject_visit_y2

        hiv_car_adherence_options = {}
        hiv_car_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male.appointment)
        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male_T0,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)

    def hiv_pos_nd_art_naive_at_bhs(self):
        """Enrollees at t0 who are HIV-positive and ART naive at BHS.
           Pima, RBD and VL required. Then Key RBD for later use in Annual survey.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T0.appointment)

        research_blood_draw_options = {}
        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male_T0.appointment)

        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male_T0.appointment)

        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male_T0,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)

        aliquot_type = AliquotType.objects.all()[0]
        site = self.study_site
        rbd = Panel.objects.get(name='Research Blood Draw')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male_T0, panel=rbd, aliquot_type=aliquot_type, site=site)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )

        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=KEYED, **research_blood_draw_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)

    def test_hiv_pos_nd_art_naive_at_ahs(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART, (i.e arv_naive) at the time of enrollment.
           Still arv_naive at AHS. Pima and VL required. RBD keyed in T0, so not required.
        """
        self.hiv_pos_nd_art_naive_at_bhs()

        self.subject_visit_male = self.annual_subject_visit_y2

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        research_blood_draw_options = {}
        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male.appointment)

        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male.appointment)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care=YES,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )

        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **research_blood_draw_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)

    def test_hiv_pos_nd_on_art_at_ahs(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART (i.e arv_naive) at the time of enrollment.
           But now on ART at T1. Pima and VL required at T1(rule: art naive at enrollment).
           RBD keyed in T0, so not required. POC VL not required at T1.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit
        #         self.hiv_result(POS, self.subject_visit_male_T0)
        pimavl_options = {}
        pimavl_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pimavl',
            appointment=self.subject_visit_male_T0.appointment)

        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male_T0,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=YES,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )

        # self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pimavl_options).count(), 1)

        aliquot_type = AliquotType.objects.all()[0]
        site = self.study_site
        rbd = Panel.objects.get(name='Research Blood Draw')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male_T0, panel=rbd, aliquot_type=aliquot_type, site=site)

#         PimaVlFactory(subject_visit=self.subject_visit_male_T0)

        self.subject_visit_male = self.annual_subject_visit_y2

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)
        research_blood_draw_options = {}
        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male.appointment)
        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male.appointment)
        pimavl_options.update(appointment=self.subject_visit_male.appointment)

        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care=YES,
            ever_recommended_arv=YES,
            ever_taken_arv=YES,
            on_arv=YES,
            arv_evidence=YES,  # this is the rule field
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **research_blood_draw_options).count(), 1)
        # self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pimavl_options).count(), 1)

        self.subject_visit_male_T2 = self.annual_subject_visit_y3

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T2.appointment)
        research_blood_draw_options = {}
        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male_T2.appointment)
        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male_T2.appointment)
        pimavl_options.update(appointment=self.subject_visit_male_T2.appointment)

        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T2,
            first_positive=None,
            medical_care=YES,
            ever_recommended_arv=YES,
            ever_taken_arv=YES,
            on_arv=YES,
            arv_evidence=YES,  # this is the rule field
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **research_blood_draw_options).count(), 1)

    def test_hiv_pos_nd_on_art_at_y3_missed_y2(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART (i.e arv_naive) at the time of enrollment.
           Misses T1. But now on ART at T2. Pima and VL required at T2(rule: art naive at enrollment).
           RBD keyed in T0, so not required. POC VL not required at T2.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit
        #         self.hiv_result(POS, self.subject_visit_male_T0)
        pimavl_options = {}
        pimavl_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pimavl',
            appointment=self.subject_visit_male_T0.appointment)

        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male_T0,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=YES,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )

        # self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pimavl_options).count(), 1)

        aliquot_type = AliquotType.objects.all()[0]
        site = self.study_site
        rbd = Panel.objects.get(name='Research Blood Draw')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male_T0, panel=rbd, aliquot_type=aliquot_type, site=site)

        self.subject_visit_male_T2 = self.annual_subject_visit_y3

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T2.appointment)
        research_blood_draw_options = {}
        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male_T2.appointment)
        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male_T2.appointment)
        pimavl_options.update(appointment=self.subject_visit_male_T2.appointment)

        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T2,
            first_positive=None,
            medical_care=YES,
            ever_recommended_arv=YES,
            ever_taken_arv=YES,
            on_arv=YES,
            arv_evidence=YES,  # this is the rule field
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **research_blood_draw_options).count(), 1)

    def test_hiv_pos_nd_not_on_art_at_bhs(self):
        """HIV Positive not on ART at T0, Should offer POC CD4, RBD and VL.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_car_adherence_options = {}
        hiv_car_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male_T0.appointment)
        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T0.appointment)

        research_blood_draw_options = {}
        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male_T0.appointment)

        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male_T0.appointment)

        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male_T0,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)

    def test_hiv_pos_nd_not_on_art_at_ahs(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART (i.e art_naive) at the time of enrollment. Pima required.
           Still HIV Positive and still not on ART at T1: Should offer POC CD4 and VL. No RBD
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_car_adherence_options = {}
        hiv_car_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male_T0.appointment)
        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T0.appointment)
        pimavl_options = {}
        pimavl_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pimavl',
            appointment=self.subject_visit_male_T0.appointment)
        research_blood_draw_options = {}
        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male_T0.appointment)
        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male_T0.appointment)

        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male_T0,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **hiv_car_adherence_options).count(), 1)
        # ART naive at the time of enrollment, in this case T0.
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )

        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)

        aliquot_type = AliquotType.objects.all()[0]
        site = self.study_site
        rbd = Panel.objects.get(name='Research Blood Draw')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male_T0, panel=rbd, aliquot_type=aliquot_type, site=site)

        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=KEYED, **research_blood_draw_options).count(), 1)

        # Move on to the first annual visit.
        self.subject_visit_male = self.annual_subject_visit_y2
        hiv_car_adherence_options.update(appointment=self.subject_visit_male.appointment)
        pimavl_options.update(appointment=self.subject_visit_male.appointment)
        pima_options.update(appointment=self.subject_visit_male.appointment)
        research_blood_draw_options.update(appointment=self.subject_visit_male.appointment)
        viral_load_options.update(appointment=self.subject_visit_male.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **research_blood_draw_options).count(), 1)

        # Move on to the second annual visit.
        self.subject_visit_male_T2 = self.annual_subject_visit_y3
        hiv_car_adherence_options.update(appointment=self.subject_visit_male_T2.appointment)
        pimavl_options.update(appointment=self.subject_visit_male_T2.appointment)
        pima_options.update(appointment=self.subject_visit_male_T2.appointment)
        research_blood_draw_options.update(appointment=self.subject_visit_male_T2.appointment)
        viral_load_options.update(appointment=self.subject_visit_male_T2.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **research_blood_draw_options).count(), 1)

    def test_hiv_pos_nd_not_on_art_at_y3_missed_y2(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART (i.e art_naive) at the time of enrollment. Pima required.
           Misses T1. Found at T2 still HIV Positive and still not on ART: Should offer POC CD4 and VL. No RBD.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        hiv_car_adherence_options = {}
        hiv_car_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male_T0.appointment)
        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T0.appointment)
        pimavl_options = {}
        pimavl_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pimavl',
            appointment=self.subject_visit_male_T0.appointment)
        research_blood_draw_options = {}
        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male_T0.appointment)
        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male_T0.appointment)

        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male_T0,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **hiv_car_adherence_options).count(), 1)
        # ART naive at the time of enrollment, in this case T0.
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )

        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)

        aliquot_type = AliquotType.objects.all()[0]
        site = self.study_site
        rbd = Panel.objects.get(name='Research Blood Draw')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male_T0, panel=rbd, aliquot_type=aliquot_type, site=site)

        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=KEYED, **research_blood_draw_options).count(), 1)

        # JUMP first annual visit. Move on to the second annual visit.
        self.subject_visit_male_T2 = self.annual_subject_visit_y3
        hiv_car_adherence_options.update(appointment=self.subject_visit_male_T2.appointment)
        pimavl_options.update(appointment=self.subject_visit_male_T2.appointment)
        pima_options.update(appointment=self.subject_visit_male_T2.appointment)
        research_blood_draw_options.update(appointment=self.subject_visit_male_T2.appointment)
        viral_load_options.update(appointment=self.subject_visit_male_T2.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **research_blood_draw_options).count(), 1)

    def test_hiv_pos_nd_on_art_at_ahs1(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART naive at the time of enrollment. Pima required.
           HIV Positive not on ART at T1: Should offer POC CD4 and VL.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male_T0,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )

        self.subject_visit_male = self.annual_subject_visit_y2

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care=YES,
            ever_recommended_arv=YES,
            ever_taken_arv=YES,
            on_arv=YES,
            arv_evidence=YES,  # this is the rule field
        )

        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)

        self.subject_visit_male_T2 = self.annual_subject_visit_y3

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T2.appointment)

        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T2,
            first_positive=None,
            medical_care=YES,
            ever_recommended_arv=YES,
            ever_taken_arv=YES,
            on_arv=YES,
            arv_evidence=YES,  # this is the rule field
        )

        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male_T2.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)

    def test_hiv_pos_nd_not_art_at_y1_misses_y2(self):
        """Previously enrollees at t0 who are HIV-positive but were ART naive at the time of enrollment. Pima required.
           Misses T2. HIV Positive and on ART at T3: Should offer POC CD4 and VL.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male_T0,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )

        self.subject_visit_male_T2 = self.annual_subject_visit_y3

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T2.appointment)

        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T2,
            first_positive=None,
            medical_care=YES,
            ever_recommended_arv=YES,
            ever_taken_arv=YES,
            on_arv=YES,
            arv_evidence=YES,  # this is the rule field
        )

        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male_T2.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)

    def hiv_pos_nd_on_art_bhs(self):
        """Enrollees at t0 who are HIV-positive and on ART at the time of enrollment.
           Pima and POC VL NOT required. RBD, VL required.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T0.appointment)

        pimavl_options = {}
        pimavl_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pimavl',
            appointment=self.subject_visit_male_T0.appointment)

        research_blood_draw_options = {}
        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male_T0.appointment)

        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male_T0.appointment)

        self.hiv_result(POS, self.subject_visit_male_T0)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=YES,
            ever_recommended_arv=YES,
            ever_taken_arv=YES,
            on_arv=YES,
            arv_evidence=YES,  # this is the rule field
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)
        #self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pimavl_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)

    def hiv_pos_nd_on_art_ahs(self):
        """Previously enrollees at t0 who are HIV-positive on ART at the time of enrollment.
           Pima and POC VL NOT required. RBD, VL required.
        """
        self.hiv_pos_nd_on_art_bhs()

        self.subject_visit_male = self.annual_subject_visit_y2

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        pimavl_options = {}
        pimavl_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pimavl',
            appointment=self.subject_visit_male.appointment)

        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **viral_load_options).count(), 1)

        self.subject_visit_male = self.annual_subject_visit_y3

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male_T2.appointment)

        pimavl_options = {}
        pimavl_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pimavl',
            appointment=self.subject_visit_male_T2.appointment)

        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male_T2.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)
        #self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pimavl_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **viral_load_options).count(), 1)

    def test_hiv_neg_bhs_and_pos_at_ahs(self):
        """ HIV Negative and in HIC at T0 and now HIV POS not on ART at T1, should Offer POC CD4, RBD and VL and PIMA VL.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        ResidencyMobilityFactory(subject_visit=self.subject_visit_male_T0)

        self.hiv_result(NEG, self.subject_visit_male_T0)

        SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
                              subject_visit=self.subject_visit_male_T0)

        HicEnrollment.objects.create(
            subject_visit=self.subject_visit_male_T0,
            report_datetime=datetime.today(),
            hic_permission=YES)

        self.subject_visit_male = self.annual_subject_visit_y2

        research_blood_draw_options = {}
        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male.appointment)

        viral_load_options = {}
        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male.appointment)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        pimavl_options = {}
        pimavl_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pimavl',
            appointment=self.subject_visit_male.appointment)

        self.hiv_result(POS, self.subject_visit_male)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)

    def hiv_pos_at_bhs_and_hiv_care_adherence_is_required(self):
        """Enrollees at t0 who are HIV-positive and on ART at the time of enrollment.
           Pima and POC VL NOT required. RBD, VL required.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        self.hiv_result(POS, self.subject_visit_male_T0)

        self.subject_visit_male = self.annual_subject_visit_y2

        hiv_care_adherence_options = {}
        hiv_care_adherence_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivcareadherence',
            appointment=self.subject_visit_male.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(
            entry_status=REQUIRED, **hiv_care_adherence_options).count(), 1)

    def test_not_known_pos_runs_hiv_and_cd4_ahs(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""
        self.subject_visit_male_T0 = self.baseline_subject_visit

        SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
                              subject_visit=self.subject_visit_male_T0)

        self.hiv_result('Declined', self.subject_visit_male_T0)

        self.subject_visit_male = self.annual_subject_visit_y2

        viral_load_options = {}
        hiv_result_options = {}
        research_blood_draw_options = {}

        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male.appointment)

        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male.appointment)
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male.appointment)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        self.hiv_result(POS, self.subject_visit_male)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **research_blood_draw_options).count(), 1)

    def test_not_known_neg_runs_hiv_and_cd4_ahs_1(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""
        self.subject_visit_male_T0 = self.baseline_subject_visit

        SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
                              subject_visit=self.subject_visit_male_T0)

        self.hiv_result(NEG, self.subject_visit_male_T0)

        self.subject_visit_male = self.annual_subject_visit_y2

        viral_load_options = {}
        hiv_result_options = {}

        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male.appointment)
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male.appointment)

        research_blood_draw_options = {}
        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male.appointment)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        self.hiv_result("Declined", self.subject_visit_male)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **viral_load_options).count(), 1)

    def test_not_known_pos_runs_hiv_and_cd4_ahs_2(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""
        self.subject_visit_male_T0 = self.baseline_subject_visit

        SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
                              subject_visit=self.subject_visit_male_T0)

        self.hiv_result(POS, self.subject_visit_male_T0)

        self.subject_visit_male = self.annual_subject_visit_y2

        viral_load_options = {}
        hiv_result_options = {}

        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male.appointment)
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male.appointment)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        self.hiv_result("Declined", self.subject_visit_male)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)


    def test_not_known_pos_runs_hiv_and_cd4_ahs_y3(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""
        self.subject_visit_male_T0 = self.baseline_subject_visit

        SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
                              subject_visit=self.subject_visit_male_T0)

        self.hiv_result('Declined', self.subject_visit_male_T0)

        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male_T0,
            has_tested="DWTA",
            when_hiv_test='1 to 5 months ago',
            has_record="Don't want to answer",
            verbal_hiv_result='not_answering',
            other_record=NO
        )

        self.subject_visit_male = self.annual_subject_visit_y2

        self.hiv_result('Declined', self.subject_visit_male)


        HivTestingHistory.objects.create(
            subject_visit=self.subject_visit_male,
            has_tested="DWTA",
            when_hiv_test='1 to 5 months ago',
            has_record="Don't want to answer",
            verbal_hiv_result='not_answering',
            other_record=NO
        )

        subject_visit_male_T2 = self.annual_subject_visit_y3

        viral_load_options = {}
        hiv_result_options = {}

        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=subject_visit_male_T2.appointment)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=subject_visit_male_T2.appointment)

        HivTestingHistory.objects.create(
            subject_visit=subject_visit_male_T2,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )

        self.hiv_result(POS, subject_visit_male_T2)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, **viral_load_options).count(), 1)

    def test_not_known_neg_runs_hiv_and_cd4_ahs(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""
        self.subject_visit_male_T0 = self.baseline_subject_visit

        SubjectLocatorFactory(registered_subject=self.subject_visit_male_T0.appointment.registered_subject,
                              subject_visit=self.subject_visit_male_T0)

        self.hiv_result('Declined', self.subject_visit_male_T0)

        self.subject_visit_male = self.annual_subject_visit_y2

        viral_load_options = {}
        hiv_result_options = {}
        research_blood_draw_options = {}

        research_blood_draw_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Research Blood Draw',
            appointment=self.subject_visit_male.appointment)

        viral_load_options.update(
            lab_entry__app_label='bcpp_lab',
            lab_entry__model_name='subjectrequisition',
            lab_entry__requisition_panel__name='Viral Load',
            appointment=self.subject_visit_male.appointment)
        hiv_result_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivresult',
            appointment=self.subject_visit_male.appointment)

        pima_options = {}
        pima_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='pima',
            appointment=self.subject_visit_male.appointment)

        self.hiv_result(NEG, self.subject_visit_male)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **pima_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **viral_load_options).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, **research_blood_draw_options).count(), 1)

    def test_hiv_pos_nd_art_naive_at_ahs_require_linkage_to_care(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART, (i.e arv_naive) at the time of enrollment.
           Still arv_naive at AHS. HIV linkage to care required.
        """
        self.hiv_pos_nd_art_naive_at_bhs()

        self.subject_visit_male = self.annual_subject_visit_y2

        linkage_to_care_options = {}
        linkage_to_care_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivlinkagetocare',
            appointment=self.subject_visit_male.appointment)

        self.hiv_result(POS, self.subject_visit_male)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care=YES,
            ever_recommended_arv=NO,
            ever_taken_arv=YES,
            on_arv=YES,
            arv_evidence=YES,  # this is the rule field
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **linkage_to_care_options).count(), 1)

    def test_newly_pos_and_not_art_bhs_not_require_linkage_to_care(self):
        """Newly HIV Positive not on ART at T0, Should not offer hiv linkage to care.
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        linkage_to_care_options = {}
        linkage_to_care_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivlinkagetocare',
            appointment=self.subject_visit_male_T0.appointment)

        self._hiv_result = self.hiv_result(POS, self.subject_visit_male_T0)

        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,
        )

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **linkage_to_care_options).count(), 1)

    def test_pos_on_art_notrequire_linkage_to_care(self):
        """If POS and on arv and have doc evidence, Hiv Linkage to care not required, not a defaulter."""

        self.subject_visit_male_T0 = self.baseline_subject_visit
        linkage_to_care_options = {}
        linkage_to_care_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivlinkagetocare',
            appointment=self.subject_visit_male_T0.appointment)

        self._hiv_result = self.hiv_result(POS, self.subject_visit_male_T0)

        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=YES,
            arv_evidence=YES,
        )

        # on art so no need for CD4
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **linkage_to_care_options).count(), 1)

    def test_known_neg_does_not_require_linkage_to_care(self):
        """If previous result is NEG, does not require hiv linkage to care.

        See rule_groups.ReviewNotPositiveRuleGroup
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit
        self.subject_visit_male = self.annual_subject_visit_y2

        linkage_to_care_options = {}
        linkage_to_care_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivlinkagetocare',
            appointment=self.subject_visit_male.appointment)

        self._hiv_result = self.hiv_result(NEG, self.subject_visit_male)
        # add HivCarAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=YES,
            arv_evidence=YES,
        )
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **linkage_to_care_options).count(), 1)

    def test_known_pos_defaulter_require_linkage_to_care(self):
        """If previous result is POS on art but no evidence.

        This is a defaulter

        See rule_groups.ReviewNotPositiveRuleGroup
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        # add HivCareAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=YES,
            on_arv=NO,
            arv_evidence=YES,  # this is the rule field
        )
        linkage_to_care_options = {}
        linkage_to_care_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivlinkagetocare',
            appointment=self.subject_visit_male_T0.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **linkage_to_care_options).count(), 1)

        self.subject_visit_male = self.annual_subject_visit_y2
        linkage_to_care_options = {}
        linkage_to_care_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivlinkagetocare',
            appointment=self.subject_visit_male.appointment)

        # add HivCareAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=YES,  # this is the rule field
        )
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=REQUIRED, **linkage_to_care_options).count(), 1)

    def test_known_pos_not_require_linkage_to_care(self):
        """If previous result is POS on art but no evidence.

        See rule_groups.ReviewNotPositiveRuleGroup
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        # add HivTestReview,
        HivTestReview.objects.create(
            subject_visit=self.subject_visit_male_T0,
            hiv_test_date=datetime.today() - timedelta(days=50),
            recorded_hiv_result=POS,
        )

        # add HivCareAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male_T0,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=YES,
            on_arv=YES,
            arv_evidence=YES,  # this is the rule field
        )
        linkage_to_care_options = {}
        linkage_to_care_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivlinkagetocare',
            appointment=self.subject_visit_male_T0.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **linkage_to_care_options).count(), 1)

        self.subject_visit_male = self.annual_subject_visit_y2
        linkage_to_care_options = {}
        linkage_to_care_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivlinkagetocare',
            appointment=self.subject_visit_male.appointment)

        # add HivCareAdherence,
        HivCareAdherence.objects.create(
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=YES,  # this is the rule field
        )
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **linkage_to_care_options).count(), 1)

    def test_known_neg_does_requires_hiv_linkage_to_care(self):
        """If previous result is NEG, does not need Hiv linkage to care.

        See rule_groups.ReviewNotPositiveRuleGroup
        """
        self.subject_visit_male_T0 = self.baseline_subject_visit

        self._hiv_result = self.hiv_result(NEG, self.subject_visit_male_T0)
        self.subject_visit_male = self.annual_subject_visit_y2

        linkage_to_care_options = {}
        linkage_to_care_options.update(
            entry__app_label='bcpp_subject',
            entry__model_name='hivlinkagetocare',
            appointment=self.subject_visit_male.appointment)

        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status=NOT_REQUIRED, **linkage_to_care_options).count(), 1)
