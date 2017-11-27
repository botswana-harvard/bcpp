"""
Django settings for bcpp project.
Generated by 'django-admin startproject' using Django 1.10.4.
For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import configparser
import os
import sys

from django.core.management.color import color_style
from pathlib import PurePath

from .logging import LOGGING

style = color_style()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_NAME = 'bcpp'

logging_handler = LOGGING.get('handlers').get('file').get('filename')
sys.stdout.write(style.SUCCESS(f'Logging to {logging_handler}\n'))

DEBUG = True

CONFIG_FILE = 'maunatlala.conf'
MYSQL_CONF = 'mysql.conf'
ETC_DIR = '/etc'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
INTERNAL_IPS = ['127.0.0.1']

CONFIG_PATH = os.path.join(ETC_DIR, APP_NAME, CONFIG_FILE)
sys.stdout.write(style.SUCCESS(f'Config folder {ETC_DIR}\n'))
sys.stdout.write(style.SUCCESS(f'  * Reading config from {CONFIG_FILE}\n'))
sys.stdout.write(style.SUCCESS(f'  * Reading mysql from {MYSQL_CONF}\n'))

config = configparser.RawConfigParser()
config.read(os.path.join(CONFIG_PATH))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['django'].get('secret_key', 'blah$blah$blah')
# SECRET_KEY = '9-%tjc_ov-=t6-fefrys4n@izkj4y8oewah6uf2p9q%*!ub%)^'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'tz_detect',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    # 'debug_toolbar',
    'django_extensions',
    'django_js_reverse',
    'django_crypto_fields.apps.AppConfig',
    'django_revision.apps.AppConfig',
    'edc_consent.apps.AppConfig',
    'edc_dashboard.apps.AppConfig',
    'edc_lab_dashboard.apps.AppConfig',
    'edc_registration.apps.AppConfig',
    'edc_reference.apps.AppConfig',
    'edc_metadata_rules.apps.AppConfig',
    'edc_sync_files.apps.AppConfig',
    'edc_visit_schedule.apps.AppConfig',
    'edc_call_manager.apps.AppConfig',
    'member_dashboard.apps.AppConfig',
    'household_dashboard.apps.AppConfig',
    'plot_dashboard.apps.AppConfig',
    'bcpp_community.apps.AppConfig',
    'bcpp_consent.apps.AppConfig',
    'bcpp_labs.apps.AppConfig',
    'bcpp_metadata_rules.apps.AppConfig',
    'bcpp_reference.apps.AppConfig',
    'bcpp_referral.apps.AppConfig',
    'bcpp_report.apps.AppConfig',
    'bcpp_status.apps.AppConfig',
    'bcpp_subject_dashboard.apps.AppConfig',
    'bcpp_subject_form_validators.apps.AppConfig',
    'bcpp_visit_schedule.apps.AppConfig',
    'bcpp.apps.BcppFollowAppConfig',
    'bcpp.apps.BcppSubjectAppConfig',
    'bcpp.apps.EdcAppointmentAppConfig',
    'bcpp.apps.EdcBaseAppConfig',
    'bcpp.apps.EdcDeviceAppConfig',
    'bcpp.apps.EdcIdentifierAppConfig',
    'bcpp.apps.EdcLabAppConfig',
    'bcpp.apps.EdcLabelAppConfig',
    'bcpp.apps.EdcMapAppConfig',
    'bcpp.apps.EdcMetadataAppConfig',
    'bcpp.apps.EdcProtocolAppConfig',
    'bcpp.apps.EdcTimepointAppConfig',
    'bcpp.apps.EdcVisitTrackingAppConfig',
    'bcpp.apps.EnumerationAppConfig',
    'bcpp.apps.HouseholdAppConfig',
    'bcpp.apps.MemberAppConfig',
    'bcpp.apps.PlotAppConfig',
    'bcpp.apps.EdcSyncAppConfig',
    'bcpp.apps.SurveyAppConfig',
    'bcpp.apps.AppConfig',
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
]


ROOT_URLCONF = f'{APP_NAME}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = f'{APP_NAME}.wsgi.application'

# ssh -f django@bhp066.bhp.org.bw -L5002:localhost:3306 -N
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(ETC_DIR, APP_NAME, MYSQL_CONF),
        },
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('tn', 'Setswana'),
    ('en', 'English'),
    ('kck', 'Ikalanga'),
    ('hbs', 'Hambukushu'),
)

TIME_ZONE = 'Africa/Gaborone'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = 'bootstrap3'
CORS_ORIGIN_ALLOW_ALL = True
REST_FRAMEWORK = {
    'PAGE_SIZE': 1,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

STATIC_ROOT = config['django'].get(
    'static_root', os.path.join(BASE_DIR, APP_NAME, 'static'))
STATIC_URL = '/static/'
if 'test' in sys.argv:
    MEDIA_ROOT = str(PurePath(BASE_DIR).parent)
else:
    MEDIA_ROOT = config['django'].get(
        'media_root', os.path.join(BASE_DIR, APP_NAME, 'media'))
MEDIA_URL = '/media/'

# etc ini file attributes
if DEBUG:
    KEY_PATH = config['django_crypto_fields'].get('key_path')
else:
    KEY_PATH = config['django_crypto_fields'].get('key_path')
GIT_DIR = BASE_DIR
CURRENT_MAP_AREA = config['edc_map'].get('map_area', 'test_community')

DEVICE_ID = config['edc_device'].get('device_id', '99')
DEVICE_ROLE = config['edc_device'].get('role')

# config['edc_label'].get('label_printer', 'label_printer')
LABEL_PRINTER = 'home_label_printer'
SURVEY_GROUP_NAME = config['survey'].get('group_name')
SURVEY_SCHEDULE_NAME = config['survey'].get('schedule_name')
DEVICE_IDS = config['edc_map'].get('device_ids')
ANONYMOUS_SURVEY = 'ano'
ANONYMOUS_CONSENT_GROUP = 'anonymous'
ANONYMOUS_ENABLED = config['bcpp'].get('anonymous_enabled')
EDC_MAP_DEVICE_IDS = config['edc_map'].get('device_ids')
EDC_LAB_REQUISITION_MODEL = 'bcpp_subject.SubjectRequisition'
VISIT_SCHEDULE_APP_LABEL = 'bcpp_subject'

EDC_SYNC_SERVER_IP = config['edc_sync'].get('server_ip')
EDC_SYNC_FILES_REMOTE_HOST = config['edc_sync_files'].get('remote_host')
EDC_SYNC_FILES_USER = config['edc_sync_files'].get('sync_user')
EDC_SYNC_FILES_USB_VOLUME = config['edc_sync_files'].get('usb_volume')

COUNTRY = 'botswana'
HOLIDAY_FILE = None
DEFAULT_APPOINTMENT_MODEL = 'bcpp_subject.appointment'
MAIN_NAVBAR_NAME = 'bcpp'

if 'test' in sys.argv:

    class DisableMigrations:

        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()
    PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)
    DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
