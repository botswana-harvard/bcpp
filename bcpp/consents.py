import arrow

from edc_consent.consent import Consent
from edc_consent.site_consents import site_consents
from edc_constants.constants import MALE, FEMALE

from django.apps import apps as django_apps

app_config = django_apps.get_app_config('edc_protocol')

subjectconsent_v1 = Consent(
    'bcpp_subject.subjectconsent',
    version='1',
    start=arrow.get(app_config.study_open_datetime, tzinfo=app_config.study_open_datetime.tzinfo).to('UTC').datetime,
    end=arrow.get(app_config.study_close_datetime, tzinfo=app_config.study_close_datetime.tzinfo).to('UTC').datetime,
    age_min=16,
    age_is_adult=18,
    age_max=64,
    gender=[MALE, FEMALE])

site_consents.register(subjectconsent_v1)
