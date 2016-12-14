from datetime import date
from dateutil.relativedelta import relativedelta
from faker import Faker
from faker.providers import BaseProvider
from model_mommy.recipe import Recipe, seq

from edc_base.utils import get_utcnow
from edc_constants.choices import YES, NO, POS, NEG, NOT_APPLICABLE

from .models import (Cancer, Cd4History, CeaEnrollmentChecklist, Circumcised, Circumcision,
                     ClinicQuestionnaire, CommunityEngagement, CorrectConsent, Demographics,
                     Education, ElisaHivResult, Enrollment, Grant, HeartAttack, HicEnrollment, 
                     HivCareAdherence, HivHealthCareCosts,
                     HivLinkageToCare, HivMedicalCare, HivResultDocumentation, HivResult,
                     HivTestReview, HivTested, HivTestingHistory, HivUntested, HospitalAdmission,
                     HouseholdComposition, Respondent, LabourMarketWages, MedicalDiagnoses,
                     NonPregnancy, OutpatientCare, Participation, PimaVl, Pima, PositiveParticipant,
                     Pregnancy, QualityOfLife, RbdDemographics, MostRecentPartner, ReproductiveHealth,
                     ResidencyMobility, ResourceUtilization, SecondPartner, Sti, StigmaOpinion,
                     Stigma, SubjectConsent, SubjectLocator, SubjectReferral, SubjectVisit,
                     SubstanceUse, TbSymptoms, ThirdPartner, Tubercolosis, Uncircumcised,
                     ViralLoadResult)


class BcppProvider(BaseProvider):

    def thirty_four_weeks_ago(self):
        return (get_utcnow() - relativedelta(weeks=34)).date()

    def twenty_five_weeks_ago(self):
        return (get_utcnow() - relativedelta(weeks=25)).date()

    def four_weeks_ago(self):
        return (get_utcnow() - relativedelta(weeks=4)).date()

    def next_month(self):
        return (get_utcnow() + relativedelta(month=1)).date()

fake = Faker()
fake.add_provider(BcppProvider)

cancer = Recipe(
    Cancer,
    date_cancer=date.today(),
    dx_cancer='Kaposi\'s sarcoma (KS)'
)

cd4history = Recipe(
    Cd4History,
    record_available=YES,
    last_cd4_count=400,
    last_cd4_drawn_date=date.today(),
)

ceaenrollmentchecklist = Recipe(
    CeaEnrollmentChecklist,
    report_datetime=get_utcnow(),
    citizen=YES,
    legal_marriage=NO,
    marriage_certificate=NO,
    marriage_certificate_no='123456789',
    community_resident=YES,
    enrollment_reason='CD4 < 50',
    cd4_date=date.today(),
    cd4_count=400,
    opportunistic_illness='Tuberculosis',
    diagnosis_date=fake.thirty_four_weeks_ago,
    date_signed=fake.thirty_four_weeks_ago,
)

circumcised = Recipe(
    Circumcised,
    circ_date=date.today(),
    when_circ=15,
    age_unit_circ='Years',
    where_circ='not_sure',
    why_circ='Prevent HIV/AIDS',
)

circumcision = Recipe(
    Circumcision,
    circumcised=YES,
    last_seen_circumcised=YES,
    circumcised_datetime=get_utcnow(),
    circumcised_location='Bokaa',
)

cliniquestionnaire = Recipe(
    ClinicQuestionnaire,
    know_hiv_status=YES,
    current_hiv_status=POS,
    on_arv=YES,
    arv_evidence=YES,
)

communityengagement = Recipe(
    CommunityEngagement,
    community_engagement='Very active',
    vote_engagement=YES,
    problems_engagement=None,
    solve_engagement=YES,
)

correctconsent = Recipe(
    CorrectConsent,
    report_datetime=get_utcnow(),
    old_first_name=fake.first_name,
    new_first_name=fake.first_name,
    old_last_name=fake.first_name,
    new_last_name=fake.first_name,
    old_initials='LL',
    new_initials='LA',
    old_dob=fake.dob_for_consenting_adult,
    new_dob=fake.dob_for_consenting_adult,
    old_gender='F',
    new_gender='M',
)

demographics = Recipe(
    Demographics,
    religion=None,
    ethnic=None,
    marital_status='Single/never married',
    num_wives=3,
    husband_wives=3,
    live_with=None,
)

education = Recipe(
    Education,
    education='Primary',
    working=YES,
    job_type='full-time',
    reason_unemployed='not looking',
    job_description='office',
    monthly_income='5000-10,000 pula',
)

elisahivresult = Recipe(
    ElisaHivResult,
    hiv_result=POS,
    hiv_result_datetime=get_utcnow(),
)

# Need to explicitly set subject_identifier and visit_code
enrollment = Recipe(
    Enrollment,
    community='Bokaa',
)

grant = Recipe(
    Grant,
    grant_number=1,
    grant_type='Child support '
)

heartattack = Recipe(
    HeartAttack,
    date_heart_attack=fake.thirty_four_weeks_ago,
    dx_heart_attack=None
)

hicenrollment = Recipe(
    HicEnrollment,
    hic_permission=YES,
    hiv_status_today=NEG,
    dob=fake.dob_for_consenting_adult,
    consent_datetime=get_utcnow(),
)

hivcareadherence = Recipe(
    HivCareAdherence,
    first_positive=date.today(),
    medical_care=YES,
    ever_recommended_arv=YES,
    ever_taken_arv=YES,
    ever_taken_arv=YES,
    first_arv=fake.thirty_four_weeks_ago,
    on_arv=YES,
    clinic_receiving_from='Bokaa',
    next_appointment_date=fake.next_month,
    arv_stop_date=get_utcnow(),
    arv_stop='Did not feel they were helping',
    adherence_4_day='Zero',
    adherence_4_wk='Good',
    arv_evidence=YES,
)

hivhealthcarecosts = Recipe(
    HivHealthCareCosts,
    hiv_medical_care=YES,
    reason_no_care='I am not ready to start',
    place_care_received='Government dispensary',
    care_regularity='2 times',
    doctor_visits='always',
)

hivlinkagetocare = Recipe(
    HivLinkageToCare,
    kept_appt=YES,
    diff_clininc=None,
    left_clininc_datetime=date.today(),
    clinic_first_datetime=date.today(),
    evidence_type_clinic='self_report_only',
    recommended_therapy=YES,
    reason_recommended='low_cd4',
    startered_therapy=YES,
    startered_therapy_date=date.today(),
    start_therapy_clininc='Bokaa',
    not_refered_clininc='Otse',
    evidence_not_refered='self_report_only'
)

hivmedicalcare = Recipe(
    HivMedicalCare,
    first_hiv_care_pos=date.today(),
    last_hiv_care_pos=date.today(),
    lowest_cd4='100-199',
)

hivresultdocumentation = Recipe(
    HivResultDocumentation,
    result_date=fake.thirty_four_weeks_ago,
    result_recorded=POS,
    result_doc_type='Tebelopele' 
)

hivresult = Recipe(
    HivResult,
    hiv_result=POS,
    hiv_result_datetime=get_utcnow,
    blood_draw_type='capillary',
    insufficient_vol=NOT_APPLICABLE,
    why_not_tested='not_sure',
)

hivtestreview = Recipe(
    HivTestReview,
    hiv_test_date=get_utcnow,
    recorded_hiv_result=POS,
)

hivtested = Recipe(
    HivTested,
    num_hiv_tests=3,
    where_hiv_test='Tebelopele VCT center',
    why_hiv_test='not_sure',
)

hivtestinghistory = Recipe(
    HivTestingHistory,
    has_tested=YES,
    when_hiv_test='1 to 5 months ago',
    has_record=YES,
    verbal_hiv_result=POS,
)

hivuntested = Recipe(
    HivUntested,
    why_no_hiv_test='I recently tested'
)

hospitaladmission = Recipe(
    HospitalAdmission,
    admission_nights=0,
    reason_hospitalized=None,
    facility_hospitalized=None,
    nights_hospitalized=0,
    healthcare_expense=0.0,
    travel_hours=None,
    total_expenses=0,
    hospitalization_costs=NO,
)

householdcomposition = Recipe(
    HouseholdComposition,
    physical_add='Bokaa',
    coordinates=12345.56,
    contact=YES,
    phone_number=72123456)

respondent = Recipe(
    Respondent,
    first_name=fake.first_name,
    relation='spouse',
    gender='M',
    age=30,
    present=YES,
    nights_outside=1
)

labourmarketwages = Recipe(
    LabourMarketWages,
    employed='government sector',
    occupation='Professional',
    job_description_change=0,
    days_worked=20,
    monthly_income='5000-10,000 pula',
    salary_payment='Fixed salary',
    household_income='5000-10,000 pula',
    other_occupation=None,
    govt_grant=NO,
    nights_out=0,
    weeks_out=NO,
    days_not_worked=0,
    days_inactivite=0,
)

medicaldiagnoses = Recipe(
    MedicalDiagnoses,
    diagnoses=None, # Many2Many
    heart_attack_record=NO,
    cancer_record=NO,
    tb_record=NO
)

nonpregnancy = Recipe(
    NonPregnancy,
    more_children=YES,
    last_birth=fake.thirty_four_weeks_ago,
    anc_last_pregnancy=YES,
    hiv_last_pregnancy=YES,
    preg_arv='Yes, AZT (single drug, twice a day)'
)

outpatientcare = Recipe(
    OutpatientCare,
    govt_health_care=YES,
    dept_care=YES,
    prvt_care=YES,
    trad_care=NO,
    care_visits=4,
    facility_visited='Government Clinic/Post',
    specific_clinic=None,
    care_reason='HIV-related care',
    outpatient_expense=5,
    travel_time='Under 0.5 hour',
    transport_expense=7.00,
    cost_cover=YES,
    waiting_hours='More than 3 hours',
)

participation = Recipe(
    Participation,
    full=YES,
    participation_type=NOT_APPLICABLE
)

pimavl = Recipe(
    PimaVl,
    report_datetime=get_utcnow,
    poc_vl_type='mobile setting',
    poc_vl_today=YES,
    poc_vl_today_other='Failed Blood Collection',
    pima_id=None,
    vl_value_quatifier='greater_than',
    poc_vl_value=200.00,
    time_of_test=get_utcnow,
    time_of_result=get_utcnow,
    easy_of_use='Very easy',
    stability=None,
)

pima = Recipe(
    Pima,
    pima_today=YES,
    pima_today_other='Failed Blood Collection',
    pima_id=12345,
    cd4_datetime=get_utcnow,
    cd4_value=400.00,
)

positiveparticipant = Recipe(
    PositiveParticipant,
    internalize_stigma='Disagree',
    internalized_stigma='Disagree',
    friend_stigma='Disagree',
    family_stigma='Disagree',
    enacted_talk_stigma='Disagree',
    enacted_respect_stigma='Disagree',
    enacted_jobs_tigma='Disagree',
)

pregnancy = Recipe(
    Pregnancy,
    anc_reg=YES,
    lnmp=fake.thirty_four_weeks_ago,
    more_children=YES,
    last_birth=fake.thirty_four_weeks_ago,
    anc_last_pregnancy=YES,
    hiv_last_pregnancy=YES,
    preg_arv='Yes, AZT (single drug, twice a day)'
)

qualityoflife = Recipe(
    QualityOfLife,
    mobility='no problems',
    self_care='no problems',
    activities='no problems',
    pain='no pain',
    anxiety='not anxious',
    health_today=80
)

rbddemographics = Recipe(
    RbdDemographics,
    religion=None,  # Many2Many
    ethnic=None,  # Many2Many
    marital_status='Single/never married',
    num_wives=1,
    husband_wives=1,
    live_with=None,  # Many2Many
)

mostrecentpartner = Recipe(
    MostRecentPartner,
    rel_type='Longterm partner',
    partner_residency='In this community',
    partner_age=31,
    partner_gender='M',
    last_sex_contact=3,
    last_sex_contact_other='Days',
    first_sex_contact=5,
    first_sex_contact_other='Days',
    regular_sex=5,
    having_sex=YES,
    having_sex_reg=YES,
    alcohol_before_sex=NO,
    partner_status=NEG,
    partner_arv=NO,
    status_disclosure=YES,
    multiple_partners=NO,
    intercourse_type='vaginal'
)

reproductivehealth = Recipe(
    ReproductiveHealth,
    number_children=3,
    menopause=NO,
    family_planning=None,  # Many2Many
    currently_pregnant=NO,
    when_pregnant=NO,
    gestational_weeks=None,
    pregnancy_hiv_tested=NOT_APPLICABLE,
    pregnancy_hiv_retested=YES,
)

residencymobility = Recipe(
    ResidencyMobility,
    length_residence='Less than 6 months',
    permanent_resident=YES,
    intend_residency=YES,
    nights_away='zero',
    cattle_postlands=NOT_APPLICABLE,
    cattle_postlands_other=None,
)

resourceutilization = Recipe(
    ResourceUtilization,
    out_patient=NO,
    hospitalized=0,
    money_spent=0.00,
    medical_cover=NO,
)

secondpartner = Recipe(
    SecondPartner,
    rel_type='Longterm partner',
    partner_residency='In this community',
    partner_age=30,
    partner_gender='M',
    last_sex_contact=1,
    first_sex_contact=5,
    regular_sex=4,
    having_sex=YES,
    having_sex_reg='Sometimes',
    alcohol_before_sex=YES,
    partner_status=NEG,
    partner_arv=NO,
    status_disclosure=YES,
    multiple_partners=NO,
    intercourse_type='Vaginal',
)

sti = Recipe(
    Sti,
    sti_dx=None,  # Many2Many
    wasting_date=date.today(),
    yeast_infection_date=date.today(),
    pneumonia_date=date.today(),
    pcp_date=date.today(),
    herpes_date=date.today()
)

stigmaopinion = Recipe(
    StigmaOpinion,
    test_community_stigma='Disagree',
    gossip_community_stigma='Disagree',
    respect_community_stigma='Disagree',
    enacted_verbal_stigma='Disagree',
    enacted_phyical_stigma='Disagree',
    enacted_family_stigma='Disagree',
    fear_stigma='Disagree',
)

stigma = Recipe(
    Stigma,
    anticipate_stigma='Disagree',
    enacted_shame_stigma='Disagree',
    saliva_stigma='Disagree',
    teacher_stigma='Disagree',
    children_stigma='Disagree',
)

subjectconsent = Recipe(
    SubjectConsent,
    household_member=None,  # fk
    gender='M',
    dob=fake.dob_for_consenting_adult,
    initials=fake.initials,
    subject_identifier=None,
    registered_subject=None,  # fk
    consent_datetime=get_utcnow,
    may_store_samples=YES,
    is_literate=YES,
    citizen=YES,
    is_verified=True,
    identity=seq('12315678'),
    confirm_identity=seq('12315678'),
    identity_type='OMANG',
    is_signed=True,
)

subjectlocator = Recipe(
    SubjectLocator,
    subject_visit=None,
    registered_subject=None,
    report_datetime=get_utcnow,
    date_signed=date.today(),
    home_visit_permission=YES,
    subject_cell='72777777',
    may_follow_up=YES,
    may_call_work=YES,
    may_contact_someone=YES,
    has_alt_contact=YES,
)

# Fields on this model are derived variables.
subjectreferral = Recipe(
    SubjectReferral,
    subject_referred=YES)

subjectvisit = Recipe(
    SubjectVisit,
    appointment=None,
    household_member=None,  # fk
    reason='scheduled'
)

substanceuse = Recipe(
    SubstanceUse,
    alcohol='Never',
    smoke=YES)

tbsymptoms = Recipe(
    TbSymptoms,
    cough=NO,
    fever=NO,
    lymph_nodes=NO,
    cough_blood=NO,
    night_sweat=NO,
    weight_loss=NO,
)

thirdpartner = Recipe(
    ThirdPartner,
    rel_type='Longterm partner',
    partner_residency='In this community',
    partner_age=30,
    partner_gender='M',
    last_sex_contact=1,
    first_sex_contact=5,
    regular_sex=4,
    having_sex=YES,
    having_sex_reg='Sometimes',
    alcohol_before_sex=YES,
    partner_status=NEG,
    partner_arv=NO,
    status_disclosure=YES,
    multiple_partners=NO,
    intercourse_type='Vaginal',
)

tubercolosis = Recipe(
    Tubercolosis,
    date_tb=fake.thirty_four_weeks_ago,
    dx_tb='Pulmonary tuberculosis',
)

uncircumcised = Recipe(
    Uncircumcised,
    circumcised=YES,
    health_benefits_smc=None, # Many2Many
    reason_circ='Circumcision never offered to me',
    future_circ=YES,
    future_reasons_smc='More information about benefits', 
    service_facilities=YES,
    aware_free='Radio',
)

viralloadresult = Recipe(
    ViralLoadResult,
    sample_id=None,  # Aliquot Identifier
    study_site='Gaborone',
    clinician_initials=fake.initials,
    collection_datetime=get_utcnow,
    received_datetime=get_utcnow,
    test_datetime=get_utcnow,
    assay_date=date.today(),
    result_value='200',
    validation_datetime=get_utcnow,
    assay_performed_by=fake.first_name,
    validated_by=fake.first_name,
    validation_reference=fake.first_name,
)
