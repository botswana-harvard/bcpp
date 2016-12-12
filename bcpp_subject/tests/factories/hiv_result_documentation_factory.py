import factory

from datetime import date, datetime

from bhp066.apps.bcpp_subject.models import HivResultDocumentation
from edc_constants.constants import POS


class HivResultDocumentationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivResultDocumentation

    report_datetime = datetime.today()
    result_date = date.today()
    result_recorded = POS
    result_doc_type = 'Tebelopele'
