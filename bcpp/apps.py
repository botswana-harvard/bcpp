import pytz
import sys

from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.apps import AppConfig as DjangoAppConfig
from django.core.management.color import color_style

from edc_base.utils import get_utcnow
from edc_base_test.apps import AppConfig as EdcBaseTestAppConfigParent
from edc_consent.apps import AppConfig as EdcConsentAppConfigParent
from edc_consent.consent_config import ConsentConfig
from edc_constants.constants import FAILED_ELIGIBILITY, MALE, FEMALE
from edc_device.apps import AppConfig as EdcDeviceAppConfigParent, DevicePermission
from edc_identifier.apps import AppConfig as EdcIdentifierAppConfigParent
# from edc_label.apps import AppConfig as EdcLabelConfigParent
from edc_map.apps import AppConfig as EdcMapAppConfigParent
from edc_metadata.apps import AppConfig as EdcMetadataAppConfigParent
from edc_protocol.apps import AppConfig as EdcProtocolAppConfigParent, SubjectType, Cap
from edc_timepoint.apps import AppConfig as EdcTimepointAppConfigParent
from edc_timepoint.timepoint import Timepoint
from edc_visit_tracking.apps import AppConfig as EdcVisitTrackingAppConfigParent
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT
from edc_device.constants import SERVER, CENTRAL_SERVER, CLIENT
from survey.apps import CurrentSurveys, CurrentSurvey, AppConfig as SurveyAppConfigParent

style = color_style()


class AppConfig(DjangoAppConfig):
    name = 'bcpp'


class EdcBaseTestAppConfig(EdcBaseTestAppConfigParent):
    consent_model = 'bcpp_subject.subjectconsent'
    survey_group_name = 'bcpp-survey'


class EdcDeviceAppConfig(EdcDeviceAppConfigParent):

    device_permissions = {
        'plot.plot': DevicePermission(
            model='plot.plot',
            create_roles=[SERVER, CENTRAL_SERVER],
            change_roles=[SERVER, CENTRAL_SERVER, CLIENT])
    }


class SurveyAppConfig(SurveyAppConfigParent):
    current_surveys = CurrentSurveys(*[
        CurrentSurvey('bcpp-survey.bcpp-year-1.bhs.test_community', 0),
        CurrentSurvey('bcpp-survey.bcpp-year-2.ahs.test_community', 1),
        CurrentSurvey('bcpp-survey.bcpp-year-3.ahs.test_community', 2)])


class EdcConsentAppConfig(EdcConsentAppConfigParent):
    if 'test' in sys.argv:
        sys.stdout.write(
            style.NOTICE(
                'WARNING! Overwriting AppConfig maternalconsent.start and end dates for tests only. \n'
                'See EdcConsentAppConfig\n'))
        testconsentstart = get_utcnow() - relativedelta(years=6)
        testconsentend = get_utcnow() - relativedelta(years=1)
    else:
        testconsentstart = None
        testconsentend = None
    consent_configs = [
        ConsentConfig(
            'bcpp_subject.subjectconsent',
            start=datetime(2013, 10, 18, 0, 0, 0, tzinfo=pytz.utc) if 'test' not in sys.argv else testconsentstart,
            end=datetime(2022, 12, 1, 0, 0, 0, tzinfo=pytz.utc) if 'test' not in sys.argv else testconsentend,
            version='1',
            age_min=16,
            age_is_adult=18,
            age_max=64,
            gender=[MALE, FEMALE]),
    ]


class EdcMapAppConfig(EdcMapAppConfigParent):
    verbose_name = 'BCPP Mappers'
    mapper_model = 'plot.plot'
    mapper_survey_model = 'survey.survey'
    landmark_model = 'bcpp.landmark'
    verify_point_on_save = False
    zoom_levels = ['14', '15', '16', '17', '18']


class EdcProtocolAppConfig(EdcProtocolAppConfigParent):
    protocol = 'BHP066'
    protocol_number = '066'
    protocol_name = 'BCPP'
    protocol_title = ''
    subject_types = {'subject': 'subject'}
    subject_types = [
        SubjectType('subject', 'Research Subject', Cap(model_name='bcpp_subject.subjectconsent', max_subjects=9999)),
    ]
    if 'test' in sys.argv:
        sys.stdout.write(
            style.NOTICE(
                'WARNING! Overwriting AppConfig study_open_datetime and study_close_datetime for tests only. \n'
                'See EdcProtocolAppConfig\n'))
        teststudyopen = get_utcnow() - relativedelta(years=3)
        teststudyclose = get_utcnow() + relativedelta(years=2)
    else:
        teststudyopen = None
        teststudyclose = None
    study_open_datetime = teststudyopen or datetime(2013, 10, 18, 0, 0, 0, tzinfo=pytz.utc)
    study_close_datetime = teststudyclose or datetime(2018, 12, 1, 0, 0, 0, tzinfo=pytz.utc)


class EdcVisitTrackingAppConfig(EdcVisitTrackingAppConfigParent):
    visit_models = {'bcpp_subject': ('subject_visit', 'bcpp_subject.subjectvisit')}


class EdcIdentifierAppConfig(EdcIdentifierAppConfigParent):
    identifier_prefix = '066'


class EdcMetadataAppConfig(EdcMetadataAppConfigParent):
    reason_field = {'bcpp_subject.subjectvisit': 'reason'}
    create_on_reasons = [SCHEDULED, UNSCHEDULED]
    delete_on_reasons = [LOST_VISIT, FAILED_ELIGIBILITY]


# class EdcLabelAppConfig(EdcLabelConfigParent):
#     default_cups_server_ip = '10.113.201.114'
#     default_printer_label = 'leslie_testing'
#     default_template_file = os.path.join(settings.STATIC_ROOT, 'bcpp', 'label_templates', 'aliquot.lbl')
#     default_label_identifier_name = ''


class EdcTimepointAppConfig(EdcTimepointAppConfigParent):
    timepoints = [
        Timepoint(
            model='td.appointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='DONE'
        ),
        Timepoint(
            model='td.historicalappointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='DONE'
        ),
    ]
