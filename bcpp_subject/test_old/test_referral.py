from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from edc_map.site_mappers import site_mappers
from edc.notification.models import Notification, NotificationPlan
from edc.export.models import ExportPlan
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from django.db.models import get_model

from bhp066.apps.bcpp_lab.models import AliquotType, Panel
from bhp066.apps.bcpp_lab.tests.factories import SubjectRequisitionFactory

from bhp066.apps.bcpp_subject.classes import SubjectReferralApptHelper, SubjectReferralHelper

from .base_scheduled_model_test_case import BaseScheduledModelTestCase
from .factories import (
    SubjectReferralFactory, ReproductiveHealthFactory,
    HivCareAdherenceFactory, HivResultFactory, CircumcisionFactory,
    PimaFactory, HivTestReviewFactory, HivTestingHistoryFactory, TbSymptomsFactory,
    HivResultDocumentationFactory)
from edc.entry_meta_data.models import CrfMetadata
from edc_constants.constants import POS, NEG, YES, NO
from edc_metadata.constants import NOT_REQUIRED, REQUIRED
from edc.export.models.export_transaction import ExportTransaction
from bcpp_subject.constants import BASELINE_SURVEY
from bcpp_subject.models import HivCareAdherence, HivTestingHistory, HivTestReview, SubjectReferral, Pima


class TestReferral(BaseScheduledModelTestCase):

    def tests_referred_hiv(self):
        """if IND refer for HIV testing"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='IND')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('', subject_referral.referral_code)

    def referral_smc1(self):
        report_datetime = self.subject_visit_male.report_datetime
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=NEG)
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('SMC-NEG', subject_referral.referral_code)

        report_datetime = self.subject_visit_male_annual.report_datetime
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male_annual,
            site=self.study_site, panel=panel,
            aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male_annual, hiv_result=NEG)
        CircumcisionFactory(subject_visit=self.subject_visit_male_annual, circumcised=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        return subject_referral

    @property
    def get_intervention(self):
        return site_mappers.get_mapper(site_mappers.current_community).intervention

    def tests_referred_smc1(self):
        """if NEG and male and NOT circumcised, refer for SMC in Y1 intervention
        and also refer in Y2 intervention"""
        if self.get_intervention:
            subject_referral = self.referral_smc1()
            self.assertIn('SMC-NEG', subject_referral.referral_code)

    def tests_referred_smc1a(self):
        """if NEG and male and NOT circumcised, refer for SMC in Y1 non-intervention
        and do not refer in Y2 non-intervention"""
        if not self.get_intervention:
            subject_referral = self.referral_smc1()
            self.assertEqual('', subject_referral.referral_code)

    def referral_smc2(self):
        report_datetime = self.subject_visit_male.report_datetime
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=NEG)
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised=YES)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertNotIn('SMC', subject_referral.referral_code)

        report_datetime = self.subject_visit_male_annual.report_datetime
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        return subject_referral

    def tests_referred_smc2(self):
        """if NEG and male and circumcised, do not refer for SMC, both Y1 and Y2 intervention"""
        if self.get_intervention:
            subject_referral = self.referral_smc2()
            self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_referred_smc2a(self):
        """if NEG and male and circumcised, do not refer for SMC, both Y1 and Y2 non-intervention"""
        if self.get_intervention:
            subject_referral = self.referral_smc2()
            self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_circumsised_y2_not_smc(self):
        """if NEG and male and not circumcised in Y1, then refer for SMC in Y1.
            Then if male circumsised in Y2 then do not refer for SMC in Y2."""
        report_datetime = self.subject_visit_male.report_datetime
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=NEG)
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('SMC', subject_referral.referral_code)

        report_datetime = self.subject_visit_male_annual.report_datetime
        CircumcisionFactory(subject_visit=self.subject_visit_male_annual, circumcised=YES)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_referred_smc3(self):
        """if new POS and male and circumcised, do not refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised=YES)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_export_referred_smc3(self):
        """if new POS and male and circumcised, do not refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised=YES)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertNotIn('SMC', subject_referral.referral_code)
        self.assertEqual(2, NotificationPlan.objects.all().count())
        self.assertEqual(2, ExportPlan.objects.all().count())
        export_plan = ExportPlan.objects.get(object_name='SubjectReferral')
        export_plan.target_path = '~/'
        export_plan.save()
        self.assertEqual(0, Notification.objects.all().count())
        #  call_command('export_transactions bcpp_subject.subjectreferral')
        #  self.assertEqual(1, Notification.objects.all().count())

    def tests_referred_smc3a(self):
        """if new POS and male and  NOT circumcised, do not refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_referred_smc4(self):
        """if UNKNOWN HIV status and male and NOT circumcised, refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC-UNK', subject_referral.referral_code)

    def referral_smc5(self):
        report_datetime = self.subject_visit_male.report_datetime
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male,
            site=self.study_site,
            panel=panel,
            aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC?UNK', subject_referral.referral_code)

        report_datetime = self.subject_visit_male_annual.report_datetime
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male_annual,
            site=self.study_site,
            panel=panel,
            aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        return subject_referral

    def tests_referred_smc5(self):
        """if UNKNOWN HIV status and male and unknown circ status, refer for SMC"""
        if self.get_intervention:
            subject_referral = self.referral_smc5()
            self.assertEqual('SMC?UNK', subject_referral.referral_code)

    def tests_referred_smc5a(self):
        """if UNKNOWN HIV status and male and unknown circ status, refer for SMC"""
        if self.get_intervention:
            subject_referral = self.referral_smc5()
            self.assertEqual('', subject_referral.referral_code)

    def tests_referred_smc6(self):
        """if UNKNOWN HIV status and male and unknown circ status, refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        # HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=NEG)
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Unsure')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC?UNK', subject_referral.referral_code)

    def tests_referred_smc5b(self):
        """if UNKNOWN HIV status and male and unknown circ status, refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='Declined')
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised='Unsure')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC?UNK', subject_referral.referral_code)

    def tests_referred_smc7(self):
        """if NEG and male and unknown circumcision status, refer for SMC"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=NEG)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual('SMC?NEG', subject_referral.referral_code)

    def tests_referred_neg_female_pregnant1(self):
        """if NEG and female, and not pregnant, do not refer"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result=NEG)
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEqual('', subject_referral.referral_code)

    def tests_referred_neg_female_pregnant2(self):
        """if NEG and female, and not pregnant, do not refer"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result=NEG,
                                 has_record=NO, other_record=NO)
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result='Declined')
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant=YES)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEqual('UNK?-PR', subject_referral.referral_code)

    def tests_referred_pos_female_pregnant(self):
        """if POS and female, pregnant, on-arv, refer ANC-POS"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result=POS)
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant=YES)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv=YES)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS#-AN', subject_referral.referral_code)

    def tests_referred_pos_female_pregnant2(self):
        """if newly POS and female, and pregnant, refer"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result=POS)
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant=YES)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv=NO, arv_evidence=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS!-PR', subject_referral.referral_code)

    def tests_referred_masa_monitoring1(self):
        """if known POS, on ART,  Cd4 lo, refer as MASA monitoring low"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result=POS)
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant=YES)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv=NO, arv_evidence=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS#-PR', subject_referral.referral_code)

    def tests_referred_masa_monitoring2(self):
        """if known POS, on ART,  Cd4 hi, refer as MASA monitoring hi"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result=POS)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv=YES, next_appointment_date=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_pos_female_pregnant3(self):
        """if POS and female, and pregnant, refer ANC-POS"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result=POS)
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant=YES)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('POS!-PR', subject_referral.referral_code)

    def tests_referred_neg_female(self):
        """if NEG and female, refer ANC-NEG"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_female, hiv_result=NEG)
        ReproductiveHealthFactory(subject_visit=self.subject_visit_female, currently_pregnant=YES)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEquals('NEG!-PR', subject_referral.referral_code)

    def tests_referred_cd4(self):
        """if POS but no other data, refer for CD4"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('TST-CD4', subject_referral.referral_code)

    def tests_referred1(self):
        """if known POS, high PIMA CD4 and art unknown, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result=POS,
                             hiv_test_date=date.today())
        PimaFactory(subject_visit=self.subject_visit_female, cd4_value=501, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        if self.get_intervention:
            self.assertIn('POS#-HI', subject_referral.referral_code)
        else:
            subject_referral = SubjectReferral.objects.all()[0]
            subject_referral.save()
            self.assertIn('POS#-HI', subject_referral.referral_code)

    def tests_referred2(self):
        """if known POS, low PIMA CD4 and art unknown, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result=POS)
        PimaFactory(subject_visit=self.subject_visit_female, cd4_value=499, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        if self.get_intervention:
            self.assertTrue(site_mappers.get_mapper(site_mappers.current_community).intervention)
            self.assertIn('POS#-LO', subject_referral.referral_code)
        else:
            self.assertFalse(site_mappers.get_mapper(site_mappers.current_community).intervention)
            subject_referral = SubjectReferral.objects.all()[0]
            subject_referral.save()
            self.assertIn('POS#-HI', subject_referral.referral_code)

    def tests_referred3(self):
        """if known NEG but not tested today, high PIMA CD4 and art unknown, female"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result=NEG)
        PimaFactory(subject_visit=self.subject_visit_female, cd4_value=501, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertEqual('TST-HIV', subject_referral.referral_code)

    def tests_referred4(self):
        """if new POS, high PIMA CD4 and art unknown, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS, hiv_result_datetime=datetime.today())
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=501, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        if self.get_intervention:
            self.assertIn('POS!-HI', subject_referral.referral_code)
        else:
            subject_referral = SubjectReferral.objects.all()[0]
            subject_referral.save()
            self.assertIn('POS!-HI', subject_referral.referral_code)

    def tests_referred5(self):
        """if new POS, low PIMA CD4 and art unknown, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS, hiv_result_datetime=datetime.today())
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=499, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        if self.get_intervention:
            self.assertIn('POS!-LO', subject_referral.referral_code)
        else:
            subject_referral = SubjectReferral.objects.all()[0]
            subject_referral.save()
            self.assertIn('POS!-HI', subject_referral.referral_code)
            pima = Pima.objects.all()[0]
            pima.cd4_value = 349
            pima.save()
            subject_referral = SubjectReferral.objects.all()[0]
            subject_referral.save()
            self.assertIn('POS!-LO', subject_referral.referral_code)

    def tests_referred_urgent1(self):
        """if existing POS, low PIMA CD4 and art unknown, urgent referral"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_male, recorded_hiv_result=POS)
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=499, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        if self.get_intervention:
            subject_referral_helper = SubjectReferralHelper(subject_referral)
            self.assertTrue(subject_referral_helper.urgent_referral)
        else:
            subject_referral = SubjectReferral.objects.all()[0]
            subject_referral.save()
            subject_referral_helper = SubjectReferralHelper(subject_referral)
            self.assertFalse(subject_referral_helper.urgent_referral)

    def tests_referred_urgent2(self):
        """if existing POS, low PIMA CD4 and art no, urgent referral"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_male, recorded_hiv_result=POS)
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=499, report_datetime=datetime.today())
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        if self.get_intervention:
            subject_referral_helper = SubjectReferralHelper(subject_referral)
            self.assertTrue(subject_referral_helper.urgent_referral)
        else:
            subject_referral = SubjectReferral.objects.all()[0]
            subject_referral.save()
            subject_referral_helper = SubjectReferralHelper(subject_referral)
            self.assertFalse(subject_referral_helper.urgent_referral)

    def tests_referred_urgent3(self):
        """if new POS, low PIMA CD4 and art unknown, urgent referral"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS, hiv_result_datetime=datetime.today())
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=499, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        if self.get_intervention:
            subject_referral_helper = SubjectReferralHelper(subject_referral)
            self.assertTrue(subject_referral_helper.urgent_referral)
        else:
            subject_referral = SubjectReferral.objects.all()[0]
            subject_referral.save()
            subject_referral_helper = SubjectReferralHelper(subject_referral)
            self.assertFalse(subject_referral_helper.urgent_referral)

    def tests_referred_ccc3(self):
        """if new pos, high PIMA CD4 and not on art, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=NO, arv_evidence=NO, ever_taken_arv=NO)
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=501, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        if self.get_intervention:
            self.assertIn('POS!-HI', subject_referral.referral_code)
        else:
            subject_referral = SubjectReferral.objects.all()[0]
            subject_referral.save()
            self.assertIn('POS!-HI', subject_referral.referral_code)

    def tests_referred_masa1(self):
        """if new pos, low PIMA CD4 and not on art, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=NO, arv_evidence=NO)
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=499, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        if self.get_intervention:
            self.assertIn('POS!-LO', subject_referral.referral_code)
        else:
            subject_referral = SubjectReferral.objects.all()[0]
            subject_referral.save()
            self.assertIn('POS!-HI', subject_referral.referral_code)
            pima = Pima.objects.all()[0]
            pima.cd4_value = 349
            pima.save()
            subject_referral = SubjectReferral.objects.all()[0]
            subject_referral.save()
            self.assertIn('POS!-LO', subject_referral.referral_code)

    def tests_referred_verbal1(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result=POS, has_record=NO,
                                 other_record=NO)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=NO, arv_evidence=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('SMC?UNK', subject_referral.referral_code)

    def tests_hiv_result1(self):
        """"""
        report_datetime = datetime.today()
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result=POS, has_record=NO,
                                 other_record=NO)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=YES, arv_evidence=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIsNone(subject_referral.hiv_result)

    def tests_hiv_result2(self):
        """"""
        report_datetime = datetime.today()
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result=POS, has_record=YES,
                                 other_record=NO)
        care_ad = HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=YES, arv_evidence=YES)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual(POS, subject_referral.hiv_result)
        self.assertEqual(care_ad.first_arv.date(), subject_referral.hiv_result_datetime.date())

    def tests_hiv_result2a(self):
        """"""
        base_line_report_datetime = self.subject_visit_male.report_datetime
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male,
                                 report_datetime=base_line_report_datetime,
                                 verbal_hiv_result=POS, has_record=YES, other_record=NO)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male,
                                report_datetime=base_line_report_datetime,
                                on_arv=YES, arv_evidence=NO)
        hiv_test_review = HivTestReviewFactory(
            subject_visit=self.subject_visit_male,
            hiv_test_date=(base_line_report_datetime + timedelta(days=-15)).date(),
            recorded_hiv_result=POS)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=base_line_report_datetime)
        self.assertEqual(POS, subject_referral.hiv_result)
        self.assertEqual(hiv_test_review.hiv_test_date, subject_referral.hiv_result_datetime.date())

        report_datetime = self.subject_visit_male_annual.report_datetime
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male_annual, on_arv=YES, arv_evidence=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        self.assertEqual(POS, subject_referral.hiv_result)
        self.assertEqual((base_line_report_datetime + timedelta(days=-15)).date(),
                         subject_referral.hiv_result_datetime.date())
        self.assertEqual(subject_referral.referral_code, 'MASA-CC')
        self.assertTrue(subject_referral.on_art)
        self.assertIsNone(subject_referral.todays_hiv_result)

    def tests_hiv_result3(self):
        """"""
        base_line_report_datetime = self.subject_visit_male.report_datetime
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male,
                                 report_datetime=base_line_report_datetime,
                                 verbal_hiv_result=POS, has_record=NO, other_record=NO)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male,
                                report_datetime=base_line_report_datetime,
                                on_arv=NO, arv_evidence=YES)
        hiv_test_review = HivTestReviewFactory(
            subject_visit=self.subject_visit_male,
            hiv_test_date=(base_line_report_datetime + timedelta(days=-15)).date(),
            recorded_hiv_result=POS)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=base_line_report_datetime)
        self.assertEqual(POS, subject_referral.hiv_result)
        self.assertEqual(hiv_test_review.hiv_test_date, subject_referral.hiv_result_datetime.date())

        report_datetime = self.subject_visit_male_annual.report_datetime
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male_annual, on_arv=YES, arv_evidence=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        self.assertEqual(POS, subject_referral.hiv_result)
        self.assertEqual((base_line_report_datetime + timedelta(days=-15)).date(),
                         subject_referral.hiv_result_datetime.date())
        self.assertEqual(subject_referral.referral_code, 'MASA-CC')
        self.assertTrue(subject_referral.on_art)

    def tests_hiv_result3a(self):
        """Evidence of being on ARV as reported on Care and Adherence does NOT confirm a verbal positive as evidence
        of HIV infection"""
        report_datetime = datetime.today()
        HivTestingHistoryFactory(
            subject_visit=self.subject_visit_male, verbal_hiv_result=POS, has_record=NO, other_record=NO)
        hiv_care_adherence = HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=NO, arv_evidence=YES)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual(POS, subject_referral.hiv_result)
#         print 'subject_referral.hiv_result_datetime = {}'.format(subject_referral.hiv_result_datetime)
        try:
            hiv_result_date = subject_referral.hiv_result_datetime.date()
        except AttributeError:
            hiv_result_date = None
        self.assertEqual(hiv_care_adherence.first_arv.date(), hiv_result_date)

    def tests_hiv_result4(self):
        """Other record confirms a verbal positive as evidence of HIV infection."""
        report_datetime = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result=POS,
                                 has_record=NO, other_record=YES)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=NO, arv_evidence=NO)
        hiv_result_documentation = HivResultDocumentationFactory(
            subject_visit=self.subject_visit_male, result_recorded=POS, result_date=last_year_date,
            result_doc_type='ART Prescription')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual(POS, subject_referral.hiv_result)
        self.assertEqual(hiv_result_documentation.result_date, subject_referral.hiv_result_datetime.date())

    def tests_hiv_result4a(self):
        """Other record confirms a verbal positive as evidence of HIV infection not on ART."""

        today_date = date.today()
        report_datetime = datetime.today()
        last_year_date = today_date - timedelta(days=365)
        HivTestingHistoryFactory(
            subject_visit=self.subject_visit_male,
            verbal_hiv_result=POS,
            has_record=NO,
            other_record=YES)
        HivResultDocumentationFactory(
            subject_visit=self.subject_visit_male,
            result_recorded=POS,
            result_date=last_year_date,
            result_doc_type='ART Prescription')
        HivCareAdherenceFactory(
            subject_visit=self.subject_visit_male, ever_taken_arv=NO, on_arv=NO, arv_evidence=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertEqual(POS, subject_referral.hiv_result)
        self.assertFalse(subject_referral.new_pos)
        self.assertTrue(subject_referral.on_art is False)
        self.assertTrue(ScheduledEntryMetaData.objects.filter(
            appointment=self.subject_visit_male.appointment,
            entry__model_name='hivresult',
            entry_status=NOT_REQUIRED).count() == 1)
        self.assertTrue(ScheduledEntryMetaData.objects.filter(
            appointment=self.subject_visit_male.appointment,
            entry__model_name='pima',
            entry_status=REQUIRED).count() == 1)

    def tests_on_art_always_true_or_false_pos(self):
        """If result is POS then on_art has to take values in [True, False] never None.
        If result is not POS then on_art has to be None as as the other two are not applicable."""
        base_line_report_datetime = self.subject_visit_male.report_datetime
        testing_history = HivTestingHistoryFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=base_line_report_datetime,
            verbal_hiv_result=POS, has_record=NO, other_record=NO)
        hiv_test_review = HivTestReviewFactory(
            subject_visit=self.subject_visit_male,
            hiv_test_date=(base_line_report_datetime + timedelta(days=-15)).date(),
            recorded_hiv_result=POS)
        care_adherance = HivCareAdherenceFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=base_line_report_datetime,
            ever_taken_arv=NO,
            on_arv=YES, arv_evidence=YES)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=base_line_report_datetime)

        self.assertEqual(POS, subject_referral.hiv_result)
        self.assertTrue(subject_referral.on_art)

        care_adherance.on_arv = NO
        care_adherance.arv_evidence = NO
        care_adherance.save()

        subject_referral.save()
        self.assertEqual(subject_referral.on_art, False)

        care_adherance.delete()
        self.assertEqual(HivCareAdherence.objects.all().count(), 0)
        hiv_test_review.delete()
        self.assertEqual(HivTestReview.objects.all().count(), 0)
        testing_history.delete()
        self.assertEqual(HivTestingHistory.objects.all().count(), 0)

        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male, site=self.study_site,
            panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=NEG)

        subject_referral.save()
        self.assertEqual(subject_referral.on_art, None)

    def tests_referred_verbal1b(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male, site=self.study_site,
            panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result=POS, other_record=YES)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=NO, arv_evidence=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('TST-CD4', subject_referral.referral_code)

    def tests_referred_verbal2(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
            aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result=POS, other_record=YES)
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=NO, arv_evidence=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('TST-CD4', subject_referral.referral_code)

    def tests_referred_verbal3(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male, site=self.study_site,
            panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result=POS, other_record=YES)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, arv_evidence=NO, ever_taken_arv=NO, on_arv=NO)
        if self.get_intervention:
            PimaFactory(subject_visit=self.subject_visit_male, cd4_value=499, report_datetime=datetime.today())
            subject_referral = SubjectReferralFactory(
                subject_visit=self.subject_visit_male,
                report_datetime=report_datetime)
            self.assertIn('POS#-LO', subject_referral.referral_code)
        else:
            PimaFactory(subject_visit=self.subject_visit_male, cd4_value=499, report_datetime=datetime.today())
            subject_referral = subject_referral = SubjectReferralFactory(
                subject_visit=self.subject_visit_male,
                report_datetime=report_datetime)
            subject_referral.save()
            self.assertIn('POS#-HI', subject_referral.referral_code)

    def tests_referred_verbal4(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
            aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result=POS, other_record=YES)
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=NO, arv_evidence=NO)
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=501, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('POS#-HI', subject_referral.referral_code)

    def tests_referred_verbal5(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
            aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result=POS, other_record=YES)
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=YES)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_verbal6(self):
        """"""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male, site=self.study_site,
            panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result=POS, other_record=YES)
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=YES)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_masa2(self):
        """if new pos, high PIMA CD4 and on art, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=YES)
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=501, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_masa3(self):
        """if pos, low CD4 and on art, """
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=YES)
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=500, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-CC', subject_referral.referral_code)

    def tests_referred_masa4(self):
        """Tests pos today but have evidence on ART"""

        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
                                  aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_male, on_arv=NO, arv_evidence=YES)
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=500, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('MASA-DF', subject_referral.referral_code)

    def tests_referred_masa5(self):
        """if pos and defaulter """

        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result=POS)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv=NO, arv_evidence=YES)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime)
        self.assertIn('MASA-DF', subject_referral.referral_code)

    def tests_subject_referral_field_attr1(self):

        report_datetime = self.subject_visit_female.report_datetime
        last_year_date = self.subject_visit_female.report_datetime - timedelta(days=365)

        HivTestReviewFactory(subject_visit=self.subject_visit_female, recorded_hiv_result=POS,
                             hiv_test_date=last_year_date)
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv=YES, arv_evidence=YES)
        if site_mappers.get_mapper(site_mappers.current_community).current_survey_slug == BASELINE_SURVEY_SLUG:
            TbSymptomsFactory(subject_visit=self.subject_visit_female)
            PimaFactory(subject_visit=self.subject_visit_female, cd4_value=500, report_datetime=report_datetime,
                        cd4_datetime=self.subject_visit_female.report_datetime)
        panel = Panel.objects.get(name='Viral Load')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, is_drawn=YES,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'),
                                  drawn_datetime=self.subject_visit_female.report_datetime)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
            referral_clinic=site_mappers.get_mapper(site_mappers.current_community).map_area,
        )
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'arv_documentation': True,
            'arv_clinic': None,
            'cd4_result': 500,
            'cd4_result_datetime': self.subject_visit_female.report_datetime,
            'circumcised': None,
            'citizen': True,
            'citizen_spouse': False,
            'direct_hiv_documentation': True,
            'gender': u'F',
            'hiv_result': POS,
            'hiv_result_datetime': last_year_date.date(),
            'indirect_hiv_documentation': None,
            'last_hiv_result': POS,
            'new_pos': False,
            'next_arv_clinic_appointment_date': None,
            'on_art': True,
            'permanent_resident': None,
            'pregnant': None,
            'referral_clinic': site_mappers.get_mapper(site_mappers.current_community).map_area,
            'referral_code': 'MASA-CC',
            'tb_symptoms': 'cough, cough_blood, night_sweat',
            'urgent_referral': False,
            'verbal_hiv_result': None,
            'vl_sample_drawn': True,
            'vl_sample_drawn_datetime': self.subject_visit_female.report_datetime}
        if site_mappers.get_mapper(site_mappers.current_community).current_survey_slug != BASELINE_SURVEY_SLUG:
            del expected['cd4_result']
            del expected['cd4_result_datetime']
            del expected['tb_symptoms']
        subject_referral_helper.subject_referral_dict[
            'hiv_result_datetime'] = subject_referral_helper.subject_referral_dict['hiv_result_datetime'].date()
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr2(self):

        report_datetime = datetime.today()
        today = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, is_drawn=YES,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'),
                                  drawn_datetime=datetime.today())
        TbSymptomsFactory(subject_visit=self.subject_visit_female)
        # verbal POS with indirect docs
        HivTestingHistoryFactory(subject_visit=self.subject_visit_female, verbal_hiv_result=POS,
                                 has_record=NO, other_record=YES)
        #
        HivResultDocumentationFactory(
            subject_visit=self.subject_visit_female, result_recorded=POS,
            result_date=last_year_date, result_doc_type='ART Prescription')
        # on ART and there are docs
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, on_arv=YES, arv_evidence=YES)
        panel = Panel.objects.get(name='Viral Load')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_female, site=self.study_site, is_drawn=YES,
            panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=today)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
            referral_clinic=site_mappers.get_mapper(site_mappers.current_community).map_area)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'arv_documentation': True,
            'arv_clinic': None,
            'cd4_result': None,
            'cd4_result_datetime': None,
            'circumcised': None,
            'citizen': True,
            'citizen_spouse': False,
            'direct_hiv_documentation': False,
            'gender': u'F',
            'hiv_result': POS,
            'hiv_result_datetime': datetime(last_year_date.year, last_year_date.month, last_year_date.day),
            'indirect_hiv_documentation': True,
            'last_hiv_result': POS,
            'new_pos': False,
            'next_arv_clinic_appointment_date': None,
            'on_art': True,
            'permanent_resident': None,
            'pregnant': None,
            'referral_clinic': site_mappers.get_mapper(site_mappers.current_community).map_area,
            'referral_code': 'MASA-CC',
            'tb_symptoms': 'cough, cough_blood, night_sweat',
            'urgent_referral': False,
            'verbal_hiv_result': POS,
            'vl_sample_drawn': True,
            'vl_sample_drawn_datetime': today}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr3(self):

        yesterday = self.subject_visit_female.report_datetime - timedelta(days=1)
        report_datetime = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
#         panel = Panel.objects.get(name='Microtube')
#         self.subject_visit_female.report_datetime = yesterday
#         SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, is_drawn=YES,
#         panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), drawn_datetime=yesterday)
        # verbal POS with indirect docs
        HivTestingHistoryFactory(subject_visit=self.subject_visit_female, report_datetime=yesterday,
                                 verbal_hiv_result=POS, has_record=NO, other_record=YES)
        # on ART and there are docs hence indirect documentations
        adherance = HivCareAdherenceFactory(subject_visit=self.subject_visit_female, report_datetime=yesterday,
                                            ever_taken_arv=YES, on_arv=NO, arv_stop_date=last_year_date,
                                            arv_evidence=YES)

        panel = Panel.objects.get(name='Viral Load')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, is_drawn=YES,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), 
                                  drawn_datetime=yesterday)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
            referral_clinic=site_mappers.get_mapper(site_mappers.current_community).map_area)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        first_arv = adherance.first_arv.date()
        adherance.first_arv = datetime.fromordinal(first_arv.toordinal())
        expected = {
            'arv_documentation': True,
            'arv_clinic': None,
            'cd4_result': None,
            'cd4_result_datetime': None,
            'circumcised': None,
            'citizen': True,
            'citizen_spouse': False,
            'direct_hiv_documentation': False,
            'gender': u'F',
            'hiv_result': POS,
            'hiv_result_datetime': adherance.first_arv.date(),
            'indirect_hiv_documentation': True,
            'last_hiv_result': POS,
            'new_pos': False,
            'next_arv_clinic_appointment_date': None,
            'on_art': True,
            'permanent_resident': None,
            'pregnant': None,
            'referral_clinic': site_mappers.get_mapper(site_mappers.current_community).map_area,
            'referral_code': 'MASA-DF',
            'tb_symptoms': '',
            'urgent_referral': True,
            'verbal_hiv_result': POS,
            'vl_sample_drawn': True,
            'vl_sample_drawn_datetime': yesterday}
        actual = subject_referral_helper.subject_referral_dict
        hiv_result_datetime = actual.get('hiv_result_datetime')
        actual.update({
            'hiv_result_datetime': hiv_result_datetime.date()
        })
        self.assertDictContainsSubset(expected, actual)

    def tests_subject_referral_field_attr4(self):

        yesterday = self.subject_visit_female.report_datetime - timedelta(days=1)
        first_arv = self.subject_visit_female.report_datetime - timedelta(days=120)
        report_datetime = datetime.today()
        today_date = date.today()
        last_year_date = today_date - timedelta(days=365)
        panel = Panel.objects.get(name='Microtube')
        self.subject_visit_female.report_datetime = yesterday
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, is_drawn=YES,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'),
                                  drawn_datetime=yesterday)
        # verbal POS with indirect docs
        HivTestingHistoryFactory(subject_visit=self.subject_visit_female, report_datetime=yesterday,
                                 verbal_hiv_result=POS, has_record=NO, other_record=NO)
        # on ART and there are docs
        HivCareAdherenceFactory(subject_visit=self.subject_visit_female, report_datetime=yesterday,
                                ever_taken_arv=YES, on_arv=NO, arv_stop_date=last_year_date, arv_evidence=YES,
                                first_arv=first_arv.date())
        panel = Panel.objects.get(name='Viral Load')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_female, site=self.study_site, is_drawn=YES,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'), 
                                  drawn_datetime=yesterday)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
            referral_clinic=site_mappers.get_mapper(site_mappers.current_community).map_area)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'arv_documentation': True,
            'arv_clinic': None,
            'cd4_result': None,
            'cd4_result_datetime': None,
            'circumcised': None,
            'citizen': True,
            'citizen_spouse': False,
            'direct_hiv_documentation': False,
            'gender': u'F',
            'hiv_result': POS,
            'hiv_result_datetime': first_arv.replace(hour=0, minute=0, second=0, microsecond=0),
            'indirect_hiv_documentation': True,
            'last_hiv_result': POS,
            'new_pos': False,  # undocumented verbal_hiv_result can suggest not a new POS
            'next_arv_clinic_appointment_date': None,
            'on_art': True,
            'permanent_resident': None,
            'pregnant': None,
            'referral_clinic': site_mappers.get_mapper(site_mappers.current_community).map_area,
            'referral_code': 'MASA-DF',
            'tb_symptoms': '',
            'urgent_referral': True,  # because this is a defaulter
            'verbal_hiv_result': POS,
            'vl_sample_drawn': True,
            'vl_sample_drawn_datetime': yesterday}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr5(self):
        """if IND refer for HIV testing"""

        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(subject_visit=self.subject_visit_male, site=self.study_site,
                                  panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(subject_visit=self.subject_visit_male, verbal_hiv_result=POS,
                                 has_record=NO, other_record=NO)
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='Declined')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'direct_hiv_documentation': False,
            'indirect_hiv_documentation': False,
            'last_hiv_result': None,  # undocumented verbal_hiv_result cannot be the last result
            'last_hiv_result_date': None,  # undocumented verbal_hiv_result cannot be the last result
            'new_pos': None,  # undocumented verbal_hiv_result can suggest not a new POS
            'verbal_hiv_result': POS,
            'hiv_result': "Declined"}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr6(self):
        """if IND refer for HIV testing"""

        report_datetime = datetime.today()
        last_date = report_datetime.date() - relativedelta(years=3)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male,
            site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(
            subject_visit=self.subject_visit_male, verbal_hiv_result=POS, has_record=YES, other_record=NO)
        HivTestReviewFactory(subject_visit=self.subject_visit_male, hiv_test_date=last_date, recorded_hiv_result=NEG)
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='Declined')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'direct_hiv_documentation': True,
            'indirect_hiv_documentation': False,
            'last_hiv_result': NEG,
            'last_hiv_result_date': last_date,
            'new_pos': None,
            'verbal_hiv_result': POS,
            'hiv_result': "Declined"}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr7(self):
        """ """

        report_datetime = datetime.today()
        last_date = report_datetime.date() - relativedelta(years=3)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male,
            site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(
            subject_visit=self.subject_visit_male, verbal_hiv_result=POS, has_record=YES, other_record=YES)
        HivTestReviewFactory(subject_visit=self.subject_visit_male, hiv_test_date=last_date, recorded_hiv_result=NEG)
        HivResultDocumentationFactory(
            subject_visit=self.subject_visit_male,
            result_date=report_datetime - relativedelta(years=1),
            result_recorded=POS, result_doc_type='Record of CD4 count')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='Declined')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'direct_hiv_documentation': True,
            'indirect_hiv_documentation': True,
            'last_hiv_result': NEG,
            'last_hiv_result_date': last_date,
            'new_pos': False,
            'verbal_hiv_result': POS,
            'hiv_result': "Declined"}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr8(self):
        """ """

        report_datetime = datetime.today()
        last_date = report_datetime.date() - relativedelta(years=3)
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male,
            site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(
            subject_visit=self.subject_visit_male, verbal_hiv_result=POS, has_record=YES, other_record=YES)
        HivTestReviewFactory(subject_visit=self.subject_visit_male, hiv_test_date=last_date, recorded_hiv_result=POS)
        HivResultDocumentationFactory(
            subject_visit=self.subject_visit_male, result_date=report_datetime - relativedelta(years=1),
            result_recorded=POS, result_doc_type='Record of CD4 count')
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result='Declined')
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'direct_hiv_documentation': True,
            'indirect_hiv_documentation': True,
            'last_hiv_result': POS,
            'last_hiv_result_date': last_date,
            'new_pos': False,
            'verbal_hiv_result': POS,
            'hiv_result': "Declined"}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def tests_subject_referral_field_attr9(self):
        """ """

        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male,
            site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        subject_referral_helper = SubjectReferralHelper(subject_referral)
        expected = {
            'direct_hiv_documentation': False,
            'indirect_hiv_documentation': None,
            'last_hiv_result': None,
            'last_hiv_result_date': None,
            'new_pos': True,
            'verbal_hiv_result': None,
            'hiv_result': POS}
        self.assertDictContainsSubset(expected, subject_referral_helper.subject_referral_dict)

    def test_export_history1(self):
        """Asserts a referral is queued for export."""
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male, site=self.study_site, panel=panel,
            aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=NEG)
        CircumcisionFactory(subject_visit=self.subject_visit_male, circumcised=NO)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertIn('SMC-NEG', subject_referral.referral_code)
        self.assertEqual(ExportTransaction.objects.filter(tx_pk=subject_referral.pk).count(), 1)

    def tests_new_pos_true(self):
        """Test that new_pos field in referral is evaluated correctly when participant tested POS today"""

        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male,
            site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS, hiv_result_datetime=datetime.today())
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=499, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertTrue(subject_referral.todays_hiv_result)
        self.assertFalse(subject_referral.indirect_hiv_documentation)
        self.assertFalse(subject_referral.direct_hiv_documentation)
        self.assertTrue(subject_referral.new_pos)

    def tests_new_pos_false1(self):
        """Test that new_pos field in referral is evaluated correctly when participant is a known POS trough
           HivTestReview"""

        report_datetime = datetime.today()
        last_date = report_datetime.date() - relativedelta(years=3)
        HivTestingHistoryFactory(
            subject_visit=self.subject_visit_male, verbal_hiv_result=POS, has_record=YES, other_record=NO)
        HivTestReviewFactory(subject_visit=self.subject_visit_male, hiv_test_date=last_date, recorded_hiv_result=POS)
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=499, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertFalse(subject_referral.todays_hiv_result)
        self.assertFalse(subject_referral.indirect_hiv_documentation)
        self.assertTrue(subject_referral.direct_hiv_documentation)
        self.assertFalse(subject_referral.new_pos)

    def tests_new_pos_false2(self):
        """Test that new_pos field in referral is evaluated correctly when participant is a known POS trough
           HivResultDocumentation"""

        report_datetime = datetime.today()
        HivTestingHistoryFactory(
            subject_visit=self.subject_visit_male, verbal_hiv_result=POS, has_record=NO, other_record=YES)
        HivResultDocumentationFactory(
            subject_visit=self.subject_visit_male, result_date=report_datetime - relativedelta(years=1),
            result_recorded=POS, result_doc_type='Record of CD4 count')
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=499, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertFalse(subject_referral.todays_hiv_result)
        self.assertTrue(subject_referral.indirect_hiv_documentation)
        self.assertFalse(subject_referral.direct_hiv_documentation)
        self.assertFalse(subject_referral.new_pos)

    def tests_new_pos_evaluated_correctly_in_annual(self):
        """Test that new_pos field in referral is evaluated correctly in y2."""

        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male,
            site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS, hiv_result_datetime=datetime.today())
        PimaFactory(subject_visit=self.subject_visit_male, cd4_value=499, report_datetime=datetime.today())
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertTrue(subject_referral.todays_hiv_result)
        self.assertFalse(subject_referral.indirect_hiv_documentation)
        self.assertFalse(subject_referral.direct_hiv_documentation)
        self.assertTrue(subject_referral.new_pos)
        subject_referral_annual = SubjectReferralFactory(
            subject_visit=self.subject_visit_male_annual,
            report_datetime=report_datetime)
        self.assertFalse(subject_referral_annual.new_pos)

    def tests_correctness_of_citizen_field(self):
        """Asserts that a citizen field is populated correctly following enrollment_checklist value."""
#         print "Here are registered subjects", RegisteredSubject.objects.filter(
#             registration_identifier=self.household_member_male.internal_identifier)
        report_datetime = datetime.today()
        panel = Panel.objects.get(name='Microtube')
        SubjectRequisitionFactory(
            subject_visit=self.subject_visit_male, site=self.study_site,
            panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
        HivTestingHistoryFactory(
            subject_visit=self.subject_visit_male, verbal_hiv_result=POS, has_record=YES, other_record=YES)
        HivResultFactory(subject_visit=self.subject_visit_male, hiv_result=POS)
        subject_referral = SubjectReferralFactory(
            subject_visit=self.subject_visit_male,
            report_datetime=report_datetime)
        self.assertTrue(subject_referral.citizen)

        HouseholdMember = get_model('member', 'HouseholdMember')
#         non_citizen_household_member_male = HouseholdMember.objects.create(
#             household_structure=self.household_structure,
#             first_name='ZEST', initials='ZP', gender='M',
#             age_in_years=30, study_resident=YES, relation='brother',
#             inability_to_participate=NOT_APPLICABLE)
#
#         self.assertEqual(RegisteredSubject.objects.filter(registration_identifier=non_citizen_household_member_male.internal_identifier).count(), 1)

#         non_citizen_enrollment_male = EnrollmentChecklistFactory(
#             household_member=non_citizen_household_member_male,
#             initials=non_citizen_household_member_male.initials,
#             gender=non_citizen_household_member_male.gender,
#             dob=date.today() - relativedelta(years=non_citizen_household_member_male.age_in_years),
#             guardian=NOT_APPLICABLE,
#             part_time_resident=YES,
#             citizen=NO,
#             legal_marriage=YES,
#             marriage_certificate=YES)
#
#         self.assertEqual(RegisteredSubject.objects.filter(registration_identifier=non_citizen_household_member_male.internal_identifier).count(), 1)
#

#         non_citizen_subject_consent_male = SubjectConsentFactory(
#             consent_datetime=datetime.today(),
#             household_member=non_citizen_household_member_male,
#             gender='M',
#             dob=non_citizen_enrollment_male.dob,
#             first_name='ZEST',
#             last_name='ZP',
#             citizen=NO,
#             initials=non_citizen_enrollment_male.initials,
#             legal_marriage=YES,
#             confirm_identity='101119813',
#             identity='101119813',
#             marriage_certificate=YES,
#             marriage_certificate_no='9999776',
#             study_site=self.study_site)
# 
#         self.assertEqual(RegisteredSubject.objects.filter(
#             registration_identifier=non_citizen_household_member_male.internal_identifier).count(), 1)
# 
#         non_citizen_appointment_male = Appointment.objects.get(
#             registered_subject=non_citizen_subject_consent_male.registered_subject,
#             visit_definition__time_point=0)
#         self.assertEqual(RegisteredSubject.objects.filter(
#             registration_identifier=non_citizen_household_member_male.internal_identifier).count(), 1)
# 
#         non_citizen_subject_visit_male = SubjectVisitFactory(
#             report_datetime=datetime.today(),
#             appointment=non_citizen_appointment_male, household_member=non_citizen_household_member_male)
# 
#         SubjectLocatorFactory(subject_visit=non_citizen_subject_visit_male)
#         SubjectRequisitionFactory(
#             subject_visit=non_citizen_subject_visit_male, site=self.study_site,
#             panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
#         HivTestingHistoryFactory(subject_visit=non_citizen_subject_visit_male,
#                                  verbal_hiv_result=POS, has_record=YES, other_record=YES)
#         self.assertEqual(RegisteredSubject.objects.filter(registration_identifier=non_citizen_household_member_male.internal_identifier).count(), 1)
#
#         non_citizen_appointment_male = Appointment.objects.get(registered_subject=non_citizen_subject_consent_male.registered_subject,
#                                                                visit_definition__time_point=0)
#         self.assertEqual(RegisteredSubject.objects.filter(registration_identifier=non_citizen_household_member_male.internal_identifier).count(), 1)
#         non_citizen_subject_visit_male = SubjectVisitFactory(
#             report_datetime=datetime.today(),
#             appointment=non_citizen_appointment_male, household_member=non_citizen_household_member_male)
#         SubjectLocatorFactory(subject_visit=non_citizen_subject_visit_male)
#         SubjectRequisitionFactory(subject_visit=non_citizen_subject_visit_male, site=self.study_site, panel=panel, aliquot_type=AliquotType.objects.get(alpha_code='WB'))
#         HivTestingHistoryFactory(subject_visit=non_citizen_subject_visit_male, verbal_hiv_result=POS, has_record=YES, other_record=YES)
#         HivResultFactory(subject_visit=non_citizen_subject_visit_male, hiv_result=POS)
#         subject_referral = SubjectReferralFactory(
#             subject_visit=non_citizen_subject_visit_male,
#             report_datetime=report_datetime)

