import sys

from django.apps import AppConfig as DjangoAppConfig

from edc_device.apps import AppConfig as EdcDeviceAppConfigParent
from edc_map.apps import AppConfig as EdcMapAppConfigParent
from edc_protocol.apps import AppConfig as EdcProtocolAppConfigParent, SubjectType, Cap
from django.core.management.color import color_style
from edc_base.utils import get_utcnow
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz

style = color_style()


class AppConfig(DjangoAppConfig):
    name = 'bcpp'


class EdcDeviceAppConfig(EdcDeviceAppConfigParent):
    device_id = '99'


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
    study_open_datetime = teststudyopen or datetime(2016, 4, 1, 0, 0, 0, tzinfo=pytz.utc)
    study_close_datetime = teststudyclose or datetime(2018, 12, 1, 0, 0, 0, tzinfo=pytz.utc)
