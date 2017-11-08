import configparser
from datetime import datetime
import os

from bcpp_follow.apps import AppConfig as BaseBcppFollowAppConfig
from bcpp_subject.apps import AppConfig as BaseBcppSubjectAppConfig
from bcpp_subject.parsers import schedule_appt_date_parser
from bcpp_subject_dashboard.apps import AppConfig as BaseBcppSubjectDashboardAppConfig
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from dateutil.tz import gettz
from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from django.core.management.color import color_style
from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
from edc_facility.facility import Facility
from edc_base.address import Address
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_base.utils import get_utcnow
from edc_constants.constants import FAILED_ELIGIBILITY
from edc_device import DevicePermissions, DeviceAddPermission, DeviceChangePermission
from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
from edc_device.constants import CENTRAL_SERVER, CLIENT, NODE_SERVER
from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
from edc_lab.apps import AppConfig as BaseEdcLabAppConfig
from edc_lab_dashboard.apps import AppConfig as BaseEdcLabDashboardAppConfig
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
from enumeration.apps import AppConfig as BaseEnumerationAppConfig
from household.apps import AppConfig as BaseHouseholdAppConfig
from household_dashboard.apps import AppConfig as BaseHouseholdDashboardAppConfig
from member.apps import AppConfig as BaseMemberAppConfig
from member_dashboard.apps import AppConfig as BaseMemberDashboardAppConfig
from plot.apps import AppConfig as BasePlotAppConfig
from plot_dashboard.apps import AppConfig as BasePlotDashboardAppConfig
from survey import S
from survey.apps import AppConfig as BaseSurveyAppConfig


style = color_style()

config = configparser.RawConfigParser()
config.read(os.path.join(settings.ETC_DIR,
                         settings.APP_NAME,
                         settings.CONFIG_FILE))


class AppConfig(DjangoAppConfig):
    name = 'bcpp'
    base_template_name = 'bcpp/base.html'
    dashboard_url_name = 'home_url'
    listboard_url_name = 'home_url'


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    protocol = 'BHP066'
    protocol_number = '066'
    protocol_name = 'BCPP'
    protocol_title = 'Botswana Combination Prevention Project'
    subject_types = [
        SubjectType('subject', 'Research Subject',
                    Cap(model_name='bcpp_subject.subjectconsent', max_subjects=99999)),
        SubjectType('subject', 'Anonymous Research Subject',
                    Cap(model_name='bcpp_subject.anonymousconsent', max_subjects=9999)),
    ]
    study_open_datetime = datetime(2013, 10, 18, 0, 0, 0, tzinfo=gettz('UTC'))
    study_close_datetime = datetime(2018, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))

    @property
    def site_name(self):
        from edc_map.site_mappers import site_mappers
        return site_mappers.current_map_area

    @property
    def site_code(self):
        from edc_map.site_mappers import site_mappers
        return site_mappers.current_map_code


class PlotDashboardAppConfig(BasePlotDashboardAppConfig):
    base_template_name = 'bcpp/base.html'


class PlotAppConfig(BasePlotAppConfig):

    @property
    def add_plot_map_areas(self):
        from edc_map.site_mappers import site_mappers
        return [site_mappers.current_map_area]


class HouseholdAppConfig(BaseHouseholdAppConfig):
    max_failed_enumeration_attempts = 10


class HouseholdDashboardAppConfig(BaseHouseholdDashboardAppConfig):
    base_template_name = 'bcpp/base.html'


class MemberAppConfig(BaseMemberAppConfig):
    pass


class MemberDashboardAppConfig(BaseMemberDashboardAppConfig):
    base_template_name = 'bcpp/base.html'


class EnumerationAppConfig(BaseEnumerationAppConfig):
    base_template_name = 'bcpp/base.html'
    subject_dashboard_url_name = 'bcpp_subject:dashboard_url'


class BcppSubjectAppConfig(BaseBcppSubjectAppConfig):
    pass


class BcppSubjectDashboardAppConfig(BaseBcppSubjectDashboardAppConfig):
    base_template_name = 'bcpp/base.html'


class BcppFollowAppConfig(BaseBcppFollowAppConfig):
    base_template_name = 'bcpp/base.html'


class EdcLabDashboardAppConfig(BaseEdcLabDashboardAppConfig):
    base_template_name = 'bcpp/base.html'


class EdcLabAppConfig(BaseEdcLabAppConfig):
    requisition_model = settings.EDC_LAB_REQUISITION_MODEL
    result_model = 'edc_lab.result'

    @property
    def study_site_name(self):
        from edc_map.site_mappers import site_mappers
        return site_mappers.current_map_area


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'BCPP'
    institution = 'Botswana-Harvard AIDS Institute Partnership'
    copyright = f'2013-{get_utcnow().year}'
    license = 'GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007'
    physical_address = Address(
        company_name='Botswana-Harvard AIDS Institute Partnership',
        address='Plot 1836',
        city='Gaborone',
        country='Botswana',
        tel='+267 3902671',
        fax='+267 3901284')
    postal_address = Address(
        company_name='Botswana-Harvard AIDS Institute Partnership',
        address='Private Bag BO 320',
        city='Bontleng',
        country='Botswana')


class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
    use_settings = True
    device_id = settings.DEVICE_ID
    device_role = settings.DEVICE_ROLE
    device_permissions = DevicePermissions(
        DeviceAddPermission(
            model='plot.plot',
            device_roles=[CENTRAL_SERVER, CLIENT]),
        DeviceChangePermission(
            model='plot.plot',
            device_roles=[NODE_SERVER, CENTRAL_SERVER, CLIENT]))


class SurveyAppConfig(BaseSurveyAppConfig):
    #     if 'test' in sys.argv:
    #         current_surveys = [
    #             S('bcpp-survey.bcpp-year-1.bhs.test_community'),
    #             S('bcpp-survey.bcpp-year-2.ahs.test_community'),
    #             S('bcpp-survey.bcpp-year-3.ahs.test_community'),
    #             S('bcpp-survey.bcpp-year-3.ess.test_community')]
    map_area = settings.CURRENT_MAP_AREA
    current_surveys = [
        S(f'bcpp-survey.bcpp-year-1.bhs.{map_area}'),
        S(f'bcpp-survey.bcpp-year-2.ahs.{map_area}'),
        S(f'bcpp-survey.bcpp-year-3.ahs.{map_area}'),
        S(f'bcpp-survey.bcpp-year-3.ess.{map_area}')]


class EdcMapAppConfig(BaseEdcMapAppConfig):
    verbose_name = 'BCPP Mappers'
    mapper_model = 'plot.plot'
    landmark_model = 'bcpp.landmark'
    verify_point_on_save = False
    zoom_levels = ['14', '15', '16', '17', '18']
    identifier_field_attr = 'plot_identifier'
    # Extra filter boolean attribute name.
    extra_filter_field_attr = 'enrolled'


class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
    report_datetime_allowance = -1  # disabled
    visit_models = {
        'bcpp_subject': ('subject_visit', 'bcpp_subject.subjectvisit')}


class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfig):
    identifier_prefix = '066'


class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
    reason_field = {'bcpp_subject.subjectvisit': 'reason'}
    create_on_reasons = [SCHEDULED, UNSCHEDULED]
    delete_on_reasons = [LOST_VISIT, FAILED_ELIGIBILITY]
    metadata_rules_enabled = True  # default


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
    server_ip = config['edc_sync'].get('server_ip')
    base_template_name = 'bcpp/base.html'
    # custom_json_parsers = [schedule_appt_date_parser]


class EdcSyncFilesAppConfig(BaseEdcSyncFilesAppConfig):
    edc_sync_files_using = True
    remote_host = config['edc_sync_files'].get('remote_host')
    user = config['edc_sync_files'].get('sync_user')
    usb_volume = config['edc_sync_files'].get('usb_volume')


class EdcLabelAppConfig(BaseEdcLabelAppConfig):
    template_folder = os.path.join(
        settings.STATIC_ROOT, 'bcpp', 'label_templates')

# from edc_base_test.apps import AppConfig as BaseEdcBaseTestAppConfig
#
# class EdcBaseTestAppConfig(BaseEdcBaseTestAppConfig):
#     consent_model = 'bcpp_subject.subjectconsent'
#     survey_group_name = 'bcpp-survey'
