import arrow

from dateutil.tz import gettz
from datetime import datetime
from django.apps import apps as django_apps
from django.conf import settings
from edc_consent.consent import Consent
from edc_consent.site_consents import site_consents
from edc_constants.constants import MALE, FEMALE

app_config = django_apps.get_app_config('edc_protocol')

tzinfo = gettz('Africa/Gaborone')

v1 = Consent(
    'bcpp_subject.subjectconsent',
    version='1',
    start=arrow.get(
        datetime(2013, 10, 18, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2014, 4, 9, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime,
    age_min=16,
    age_is_adult=18,
    age_max=64,
    gender=[MALE, FEMALE])

v2 = Consent(
    'bcpp_subject.subjectconsent',
    version='2',
    # updates_versions=['1'],
    start=arrow.get(
        datetime(2014, 4, 10, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2015, 4, 30, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime,
    age_min=16,
    age_is_adult=18,
    age_max=64,
    gender=[MALE, FEMALE])

v3 = Consent(
    'bcpp_subject.subjectconsent',
    version='3',
    # updates_versions=['2'],
    start=arrow.get(
        datetime(2015, 5, 1, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2015, 9, 15, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime,
    age_min=16,
    age_is_adult=18,
    age_max=64,
    gender=[MALE, FEMALE])

v4 = Consent(
    'bcpp_subject.subjectconsent',
    version='4',
    # updates_versions=['3'],
    start=arrow.get(
        datetime(2015, 9, 16, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2016, 5, 22, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime,
    age_min=16,
    age_is_adult=18,
    age_max=64,
    gender=[MALE, FEMALE])

v5 = Consent(
    'bcpp_subject.subjectconsent',
    version='5',
    # updates_versions=['4'],
    start=arrow.get(
        datetime(2016, 5, 23, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2018, 4, 30, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime,
    age_min=16,
    age_is_adult=18,
    age_max=64,
    gender=[MALE, FEMALE])

anonymous_v1 = Consent(
    'bcpp_subject.anonymousconsent',
    version='1',
    group=settings.ANONYMOUS_CONSENT_GROUP,
    # updates_versions=['4'],
    start=arrow.get(
        datetime(2016, 5, 23, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2017, 12, 31, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime,
    age_min=16,
    age_is_adult=18,
    age_max=64,
    gender=[MALE, FEMALE])

clinic_v1 = Consent(
    'bcpp_clinic.clinicconsent',
    group='clinic',
    start=arrow.get(
        datetime(2013, 10, 18, 0, 0, 0), tzinfo=tzinfo).to('UTC').datetime,
    end=arrow.get(
        datetime(2018, 4, 30, 23, 59, 59), tzinfo=tzinfo).to('UTC').datetime,
    age_min=16,
    age_is_adult=18,
    age_max=64,
    gender=[MALE, FEMALE])

site_consents.register(v1, v2, v3, v4, v5, anonymous_v1, clinic_v1)
