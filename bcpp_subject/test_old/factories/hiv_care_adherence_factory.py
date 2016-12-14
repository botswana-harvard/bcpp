import factory

from datetime import datetime, timedelta

from bhp066.apps.bcpp_subject.models import HivCareAdherence
from edc_constants.constants import YES, NO


class HivCareAdherenceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivCareAdherence

    report_datetime = datetime.today()
    medical_care = YES
    ever_taken_arv = NO
    # why_no_arv_other = factory.Sequence(lambda n: 'why_no_arv_other{0}'.format(n))
    on_arv = YES
    arv_stop_other = factory.Sequence(lambda n: 'arv_stop_other{0}'.format(n))
    arv_evidence = YES
    first_arv = datetime.today() - timedelta(days=60)
