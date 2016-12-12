from datetime import datetime

from edc_constants.constants import YES, NEG

from bhp066.apps.bcpp_subject.models import HicEnrollment

from .base_scheduled_model_factory import BaseScheduledModelFactory


class HicEnrollmentFactory(BaseScheduledModelFactory):
    FACTORY_FOR = HicEnrollment

    report_datetime = datetime.today()
    hic_permission = YES
    permanent_resident = True
    intend_residency = True
    hiv_status_today = NEG
    dob = datetime(1990, 01, 01)
    household_residency = True
    citizen_or_spouse = True
    locator_information = True
    consent_datetime = datetime.today()
