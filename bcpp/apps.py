from datetime import datetime
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from dateutil.tz import gettz

from django.apps import AppConfig as DjangoAppConfig
from django.core.management.color import color_style

# from edc_label.apps import AppConfig as EdcLabelConfigParent
from edc_appointment.apps import AppConfig as EdcAppointmentAppConfigParent
from edc_appointment.facility import Facility
from edc_base.apps import AppConfig as EdcBaseAppConfigParent
from edc_base_test.apps import AppConfig as EdcBaseTestAppConfigParent
from edc_constants.constants import FAILED_ELIGIBILITY
from edc_device.apps import AppConfig as EdcDeviceAppConfigParent, DevicePermission
from edc_device.constants import SERVER, CENTRAL_SERVER, CLIENT
from edc_identifier.apps import AppConfig as EdcIdentifierAppConfigParent
from edc_map.apps import AppConfig as EdcMapAppConfigParent
from edc_metadata.apps import AppConfig as EdcMetadataAppConfigParent
from edc_protocol.apps import AppConfig as EdcProtocolAppConfigParent, SubjectType, Cap
from edc_timepoint.apps import AppConfig as EdcTimepointAppConfigParent
from edc_timepoint.timepoint import Timepoint
from edc_visit_tracking.apps import AppConfig as EdcVisitTrackingAppConfigParent
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT

from bcpp_subject.apps import AppConfig as BcppSubjectAppConfigParent
from enumeration.apps import AppConfig as EnumerationAppConfigParent
from household.apps import AppConfig as HouseholdAppConfigParent
from member.apps import AppConfig as MemberAppConfigParent
from plot.apps import AppConfig as PlotAppConfigParent
from survey.apps import AppConfig as SurveyAppConfigParent
from survey import S
from edc_base.utils import get_utcnow

style = color_style()


class AppConfig(DjangoAppConfig):
    name = 'bcpp'


class PlotAppConfig(PlotAppConfigParent):
    listboard_template_name = 'bcpp/plot_listboard.html'


class HouseholdAppConfig(HouseholdAppConfigParent):
    listboard_template_name = 'bcpp/household_listboard.html'


class MemberAppConfig(MemberAppConfigParent):
    listboard_template_name = 'bcpp/member_listboard.html'


class EnumerationAppConfig(EnumerationAppConfigParent):
    listboard_template_name = 'bcpp/enumeration_listboard.html'
    enumeration_dashboard_base_html = 'bcpp/base.html'


class BcppSubjectAppConfig(BcppSubjectAppConfigParent):
    listboard_template_name = 'bcpp/bcpp_subject_listboard.html'


class EdcBaseAppConfig(EdcBaseAppConfigParent):
    project_name = 'BCPP'
    institution = 'Botswana-Harvard AIDS Institute'
    copyright = '2013-{}'.format(get_utcnow().year)
    license = None


class EdcBaseTestAppConfig(EdcBaseTestAppConfigParent):
    consent_model = 'bcpp_subject.subjectconsent'
    survey_group_name = 'bcpp-survey'


class EdcDeviceAppConfig(EdcDeviceAppConfigParent):
    device_id = 99
    device_permissions = {
        'plot.plot': DevicePermission(
            model='plot.plot',
            create_roles=[SERVER, CENTRAL_SERVER],
            change_roles=[SERVER, CENTRAL_SERVER, CLIENT])
    }


class SurveyAppConfig(SurveyAppConfigParent):
    current_surveys = [
        S('bcpp-survey.bcpp-year-3.ahs.test_community'),
        S('bcpp-survey.bcpp-year-3.ess.test_community')]


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
    subject_types = [
        SubjectType('subject', 'Research Subject',
                    Cap(model_name='bcpp_subject.subjectconsent', max_subjects=9999)),
    ]
    study_open_datetime = datetime(2013, 10, 18, 0, 0, 0, tzinfo=gettz('UTC'))
    study_close_datetime = datetime(2018, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))


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

class EdcAppointmentAppConfig(EdcAppointmentAppConfigParent):
    app_label = 'bcpp_subject'
    default_appt_type = 'home'
    facilities = {
        'home': Facility(name='home', days=[MO, TU, WE, TH, FR, SA, SU],
                         slots=[99999, 99999, 99999, 99999, 99999, 99999, 99999])}


class EdcTimepointAppConfig(EdcTimepointAppConfigParent):
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
