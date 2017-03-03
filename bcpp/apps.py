import os
import sys

from datetime import datetime
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from dateutil.tz import gettz

from django.apps import AppConfig as DjangoAppConfig
from django.core.management.color import color_style
from django.conf import settings

from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
from edc_appointment.facility import Facility
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_base_test.apps import AppConfig as BaseEdcBaseTestAppConfig
from edc_base.utils import get_utcnow
from edc_constants.constants import FAILED_ELIGIBILITY
from edc_consent.apps import AppConfig as BaseEdcConsentAppConfig
from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig, DevicePermission
from edc_device.constants import SERVER, CENTRAL_SERVER, CLIENT
from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
from edc_lab.apps import AppConfig as BaseEdcLabAppConfig
from edc_label.apps import AppConfig as BaseEdcLabelAppConfig
from edc_map.apps import AppConfig as BaseEdcMapAppConfig
from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig, SubjectType, Cap
from edc_sync.apps import AppConfig as BaseEdcSyncAppConfig
from edc_sync_files.apps import AppConfig as BaseEdcSyncFilesAppConfig
from edc_timepoint.apps import AppConfig as BaseEdcTimepointAppConfig
from edc_timepoint.timepoint import Timepoint
from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT

from bcpp_subject.apps import AppConfig as BaseBcppSubjectAppConfig
from enumeration.apps import AppConfig as BaseEnumerationAppConfig
from household.apps import AppConfig as BaseHouseholdAppConfig
from member.apps import AppConfig as BaseMemberAppConfig
from plot.apps import AppConfig as BasePlotAppConfig
from survey.apps import AppConfig as BaseSurveyAppConfig
from survey import S

from .navbars import navbars

style = color_style()
ANONYMOUS_CONSENT_GROUP = 'anonymous'


class AppConfig(DjangoAppConfig):
    name = 'bcpp'
    base_template_name = 'bcpp/base.html'


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    protocol = 'BHP066'
    protocol_number = '066'
    protocol_name = 'BCPP'
    protocol_title = ''
    subject_types = [
        SubjectType('subject', 'Research Subject',
                    Cap(model_name='bcpp_subject.subjectconsent', max_subjects=9999)),
    ]
    study_open_datetime = datetime(2013, 10, 18, 0, 0, 0, tzinfo=gettz('UTC'))
    study_close_datetime = datetime(2018, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))


class PlotAppConfig(BasePlotAppConfig):
    base_template_name = 'bcpp/base.html'


class HouseholdAppConfig(BaseHouseholdAppConfig):
    base_template_name = 'bcpp/base.html'


class MemberAppConfig(BaseMemberAppConfig):
    base_template_name = 'bcpp/base.html'


class EnumerationAppConfig(BaseEnumerationAppConfig):
    base_template_name = 'bcpp/base.html'
    subject_dashboard_url_name = 'bcpp_subject:dashboard_url'


class BcppSubjectAppConfig(BaseBcppSubjectAppConfig):
    base_template_name = 'bcpp/base.html'


class EdcLabAppConfig(BaseEdcLabAppConfig):
    base_template_name = 'bcpp/base.html'
    requisition_model = 'bcpp_subject.subjectrequisition'
    result_model = 'edc_lab.result'


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'BCPP'
    institution = 'Botswana-Harvard AIDS Institute'
    copyright = '2013-{}'.format(get_utcnow().year)
    license = None

    def get_navbars(self):
        return navbars


class EdcBaseTestAppConfig(BaseEdcBaseTestAppConfig):
    consent_model = 'bcpp_subject.subjectconsent'
    survey_group_name = 'bcpp-survey'


class EdcConsentAppConfig(BaseEdcConsentAppConfig):
    anonymous_consent_group = ANONYMOUS_CONSENT_GROUP


class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
    device_id = 99
    device_permissions = {
        'plot.plot': DevicePermission(
            model='plot.plot',
            create_roles=[SERVER, CENTRAL_SERVER],
            change_roles=[SERVER, CENTRAL_SERVER, CLIENT])
    }


class SurveyAppConfig(BaseSurveyAppConfig):
    if 'test' in sys.argv:
        current_surveys = [
            S('bcpp-survey.bcpp-year-1.bhs.test_community'),
            S('bcpp-survey.bcpp-year-2.ahs.test_community'),
            S('bcpp-survey.bcpp-year-3.ahs.test_community'),
            S('bcpp-survey.bcpp-year-3.ess.test_community')]
    else:
        # FIXME: update for production to only included bcpp-year-3
        current_surveys = [
            S('bcpp-survey.bcpp-year-1.bhs.test_community'),
            S('bcpp-survey.bcpp-year-2.ahs.test_community'),
            S('bcpp-survey.bcpp-year-3.ahs.test_community'),
            S('bcpp-survey.bcpp-year-3.ess.test_community')]
    current_survey_schedule = 'bcpp-survey.bcpp-year-3.test_community'


class EdcMapAppConfig(BaseEdcMapAppConfig):
    verbose_name = 'BCPP Mappers'
    mapper_model = 'plot.plot'
    landmark_model = 'bcpp.landmark'
    verify_point_on_save = False
    zoom_levels = ['14', '15', '16', '17', '18']


class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
    visit_models = {
        'bcpp_subject': ('subject_visit', 'bcpp_subject.subjectvisit')}


class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfig):
    identifier_prefix = '066'


class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
    reason_field = {'bcpp_subject.subjectvisit': 'reason'}
    create_on_reasons = [SCHEDULED, UNSCHEDULED]
    delete_on_reasons = [LOST_VISIT, FAILED_ELIGIBILITY]


class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
    app_label = 'bcpp_subject'
    default_appt_type = 'home'
    facilities = {
        'home': Facility(name='home', days=[MO, TU, WE, TH, FR, SA, SU],
                         slots=[99999, 99999, 99999, 99999, 99999, 99999, 99999])}


class EdcTimepointAppConfig(BaseEdcTimepointAppConfig):
    timepoints = [
        Timepoint(
            model='bcpp_subject.appointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='DONE'
        ),
        Timepoint(
            model='bcpp_subject.historicalappointment',
            datetime_field='appt_datetime',
            status_field='appt_status',
            closed_status='DONE'
        ),
    ]


class EdcSyncAppConfig(BaseEdcSyncAppConfig):
    edc_sync_files_using = True
    role = CLIENT
    server_ip = '192.168.1.85'


class EdcSyncFilesAppConfig(BaseEdcSyncFilesAppConfig):
    edc_sync_files_using = True
    role = CLIENT
    #
    user = 'django'
    host = '192.168.1.85'
    password = None
    source_folder = os.path.join(
        settings.MEDIA_ROOT, 'transactions', 'outgoing')
    destination_folder = os.path.join(
        settings.MEDIA_ROOT, 'transactions', 'outgoing')
    archive_folder = os.path.join(
        settings.MEDIA_ROOT, 'transactions', 'archive')


class EdcLabelAppConfig(BaseEdcLabelAppConfig):
    default_cups_server_ip = '10.113.201.248'
    default_printer_label = 'aliquot'
    extra_templates_folder = os.path.join(
        settings.STATIC_ROOT, 'bcpp', 'label_templates')
#     default_template_file = os.path.join(settings.STATIC_ROOT, 'bcpp', 'label_templates', 'aliquot.lbl')
