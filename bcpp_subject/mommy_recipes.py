from datetime import date
from dateutil.relativedelta import relativedelta
from faker import Faker
from faker.providers import BaseProvider
from model_mommy.recipe import Recipe

from edc_base.utils import get_utcnow
from edc_constants.choices import YES, NO, POS, NEG

from .models import (Cancer, Cd4History, CeaEnrollmentChecklist, Circumcised, Circumcision,
                     ClinicQuestionnaire, CommunityEngagement, CorrectConsent, Demographics,
                     DetailedSexualHistory, Education, ElisaHivResult, Enrollment,
                     Grant, HeartAttack, HicEnrollment, HivCareAdherence)


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

detailedsexualhistory = Recipe(
    DetailedSexualHistory,
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
