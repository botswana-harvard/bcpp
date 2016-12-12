from edc_rule_groups import site_rule_groups
from edc_rule_groups.crf_rule import CrfRule
from edc_rule_groups.decorators import register
from edc_rule_groups.logic import Logic
from edc_rule_groups.requisition_rule import RequisitionRule
from edc_rule_groups.rule_group import RuleGroup

from .rule_group_funcs import (
    evaluate_ever_had_sex_for_female,
    func_art_naive_at_annual_or_defaulter,
    func_hiv_indeterminate_today,
    func_hiv_neg_bhs,
    func_hiv_positive_today,
    func_hiv_untested,
    func_known_pos_in_prev_year,
    func_no_verbal_hiv_result,
    func_rbd,
    func_require_pima,
    func_should_not_show_circumsition,
    func_show_hic_enrollment,
    func_show_microtube,
    func_todays_hiv_result_required,
    func_vl,
    is_gender_male)
from .models import (
    ResourceUtilization, HivTestingHistory,
    SexualBehaviour, HivCareAdherence, Circumcision,
    HivTestReview, ReproductiveHealth, MedicalDiagnoses,
    HivResult, HivResultDocumentation, ElisaHivResult, SubjectVisit,
    RegisteredSubject)


@register()
class RegisteredSubjectRuleGroup(RuleGroup):

    gender_circumsion = CrfRule(
        logic=Logic(
            predicate=func_should_not_show_circumsition,
            consequence='not_required',
            alternative='new'),
        target_model=['circumcision', 'circumcised', 'uncircumcised'])

    gender_menopause = CrfRule(
        logic=Logic(
            predicate=is_gender_male,
            consequence='not_required',
            alternative='new'),
        target_model=['reproductivehealth', 'pregnancy', 'nonpregnancy'])

    known_pos_in_y1 = CrfRule(
        logic=Logic(
            predicate=func_known_pos_in_prev_year,
            consequence='not_required',
            alternative='new'),
        target_model=['hivtestreview', 'hivtested', 'hivtestinghistory', 'hivresultdocumentation', 'hivresult', 'hivuntested'])

    pima_art_naive_enrollment_req_ahs = CrfRule(
        logic=Logic(
            predicate=func_require_pima,
            consequence='new',
            alternative='not_required'),
        target_model=['pima'])

    hiv_linkage_to_care = CrfRule(
        logic=Logic(
            predicate=func_hiv_neg_bhs,
            consequence='not_required',
            alternative='new'),
        target_model=['hivlinkagetocare'])

    require_microtube = RequisitionRule(
        logic=Logic(
            predicate=func_show_microtube,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube'])

    vl_for_pos = RequisitionRule(
        logic=Logic(
            predicate=func_vl,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Viral Load'], )

    rbd_for_pos = RequisitionRule(
        logic=Logic(
            predicate=func_rbd,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Research Blood Draw'], )

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = None
        source_model = RegisteredSubject


@register()
class ResourceUtilizationRuleGroup(RuleGroup):

    out_patient = CrfRule(
        logic=Logic(
            predicate=(('out_patient', 'equals', 'no'), ('out_patient', 'equals', 'Refuse', 'or')),
            consequence='not_required',
            alternative='new'),
        target_model=['outpatientcare'])

    hospitalized = CrfRule(
        logic=Logic(
            predicate=('hospitalized', 'equals', 0),
            consequence='not_required',
            alternative='new'),
        target_model=['hospitaladmission'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = ResourceUtilization


@register()
class HivTestingHistoryRuleGroup(RuleGroup):

    has_record = CrfRule(
        logic=Logic(
            predicate=('has_record', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivtestreview'])

    has_tested = CrfRule(
        logic=Logic(
            predicate=('has_tested', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivtested'])

    hiv_untested = CrfRule(
        logic=Logic(
            predicate=func_hiv_untested,
            consequence='new',
            alternative='not_required'),
        target_model=['hivuntested'])

    other_record = CrfRule(
        logic=Logic(
            predicate=('other_record', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivresultdocumentation'])

    require_todays_hiv_result = CrfRule(
        logic=Logic(
            predicate=func_show_microtube,
            consequence='new',
            alternative='not_required'),
        target_model=['hivresult'])

    verbal_hiv_result_hiv_care_baseline = CrfRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'POS'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivcareadherence', 'positiveparticipant', 'hivmedicalcare', 'hivhealthcarecosts'])

    verbal_response = CrfRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'NEG'),
            consequence='new',
            alternative='not_required'),
        target_model=['stigma', 'stigmaopinion'])

    other_response = CrfRule(
        logic=Logic(
            predicate=func_no_verbal_hiv_result,
            consequence='not_required',
            alternative='none'),
        target_model=['hivcareadherence', 'hivmedicalcare', 'positiveparticipant', 'stigma', 'stigmaopinion'])

    def method_result(self):
        return True

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivTestingHistory


@register()
class ReviewPositiveRuleGroup(RuleGroup):

    recorded_hiv_result = CrfRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='not_required',
            alternative='new'),
        target_model=['hivcareadherence', 'hivmedicalcare', 'positiveparticipant'])

    recorded_hivresult = CrfRule(
        logic=Logic(
            predicate=('recorded_hiv_result', 'equals', 'NEG'),
            consequence='new',
            alternative='not_required'),
        target_model=['stigma', 'stigmaopinion'])

    require_todays_hiv_result = CrfRule(
        logic=Logic(
            predicate=func_show_microtube,
            consequence='new',
            alternative='not_required'),
        target_model=['hivresult'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivTestReview


@register()
class HivCareAdherenceRuleGroup(RuleGroup):

    medical_care = CrfRule(
        logic=Logic(
            predicate=('medical_care', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivmedicalcare'])

    pima_for_art_naive = CrfRule(
        logic=Logic(
            predicate=func_require_pima,
            consequence='new',
            alternative='not_required'),
        target_model=['pima'])

    require_todays_hiv_result = CrfRule(
        logic=Logic(
            predicate=func_show_microtube,
            consequence='new',
            alternative='not_required'),
        target_model=['hivresult'])

    hiv_linkage_to_care_art_naive = CrfRule(
        logic=Logic(
            predicate=func_art_naive_at_annual_or_defaulter,
            consequence='new',
            alternative='not_required'),
        target_model=['hivlinkagetocare'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivCareAdherence


@register()
class SexualBehaviourRuleGroup(RuleGroup):

    partners = CrfRule(
        logic=Logic(
            predicate=('last_year_partners', 'gte', 1),
            consequence='new',
            alternative='not_required'),
        target_model=['monthsrecentpartner', 'monthssecondpartner', 'monthsthirdpartner'])

    last_year_partners = CrfRule(
        logic=Logic(
            predicate=('last_year_partners', 'gte', 2),
            consequence='new',
            alternative='not_required'),
        target_model=['monthssecondpartner'])

    more_partners = CrfRule(
        logic=Logic(
            predicate=('last_year_partners', 'gte', 3),
            consequence='new',
            alternative='not_required'),
        target_model=['monthsthirdpartner'])

    ever_sex = CrfRule(
        logic=Logic(
            predicate=evaluate_ever_had_sex_for_female,
            consequence='new',
            alternative='not_required'),
        target_model=['reproductivehealth', 'pregnancy', 'nonpregnancy'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = SexualBehaviour


@register()
class CircumcisionRuleGroup(RuleGroup):

    circumcised = CrfRule(
        logic=Logic(
            predicate=('circumcised', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['circumcised'])

    uncircumcised = CrfRule(
        logic=Logic(
            predicate=('circumcised', 'equals', 'No'),
            consequence='new',
            alternative='not_required'),
        target_model=['uncircumcised'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = Circumcision


@register()
class ReproductiveRuleGroup(RuleGroup):

    currently_pregnant = CrfRule(
        logic=Logic(
            predicate=(('currently_pregnant', 'equals', 'Yes'), ('menopause', 'equals', 'No', 'and')),
            consequence='new',
            alternative='not_required'),
        target_model=['pregnancy'])

    non_pregnant = CrfRule(
        logic=Logic(
            predicate=(('currently_pregnant', 'equals', 'No'), ('menopause', 'equals', 'No', 'and')),
            consequence='new',
            alternative='not_required'),
        target_model=['nonpregnancy'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = ReproductiveHealth


@register()
class MedicalDiagnosesRuleGroup(RuleGroup):
    """"Allows the heartattack, cancer, tb forms to be made available whether or not the participant
    has a record. see redmine 314."""
    heart_attack_record = CrfRule(
        logic=Logic(
            predicate=('heart_attack_record', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['heartattack'])

    cancer_record = CrfRule(
        logic=Logic(
            predicate=('cancer_record', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['cancer'])

    tb_record_tubercolosis = CrfRule(
        logic=Logic(
            predicate=('tb_record', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['tubercolosis'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = MedicalDiagnoses


class BaseRequisitionRuleGroup(RuleGroup):
    """Ensures an RBD requisition if HIV result is POS."""
    rbd_for_pos = RequisitionRule(
        logic=Logic(
            predicate=func_rbd,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Research Blood Draw'], )

    vl_for_pos = RequisitionRule(
        logic=Logic(
            predicate=func_vl,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Viral Load'], )

    """Ensures a Microtube is not required for POS."""
    microtube_for_neg = RequisitionRule(
        logic=Logic(
            predicate=func_show_microtube,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube'], )

    pima_for_art_naive = CrfRule(
        logic=Logic(
            predicate=func_require_pima,
            consequence='new',
            alternative='not_required'),
        target_model=['pima'])

    hic = CrfRule(
        logic=Logic(
            predicate=func_show_hic_enrollment,
            consequence='new',
            alternative='not_required'),
        target_model=['hicenrollment'])

    class Meta:
        abstract = True


@register()
class RequisitionRuleGroup1(BaseRequisitionRuleGroup):

    """Ensures an ELISA blood draw requisition if HIV result is IND."""
    elisa_for_ind = RequisitionRule(
        logic=Logic(
            predicate=func_hiv_indeterminate_today,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['ELISA', ], )

    """Ensures a venous blood draw requisition is required if insufficient
    volume in the capillary (microtube)."""
    venous_for_vol = RequisitionRule(
        logic=Logic(
            predicate=(('insufficient_vol', 'equals', 'Yes'), ('blood_draw_type', 'equals', 'venous', 'or'),),
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Venous (HIV)'], )

    serve_sti_form = CrfRule(
        logic=Logic(
            predicate=func_hiv_positive_today,
            consequence='new',
            alternative='not_required'),
        target_model=['sti'])

    elisa_result = CrfRule(
        logic=Logic(
            predicate=func_hiv_indeterminate_today,
            consequence='new',
            alternative='not_required'),
        target_model=['elisahivresult'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivResult


@register()
class RequisitionRuleGroup2(BaseRequisitionRuleGroup):

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivTestingHistory


@register()
class RequisitionRuleGroup3(BaseRequisitionRuleGroup):

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivTestReview


@register()
class RequisitionRuleGroup4(BaseRequisitionRuleGroup):

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivResultDocumentation


@register()
class RequisitionRuleGroup5(BaseRequisitionRuleGroup):

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = ElisaHivResult
