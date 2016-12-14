import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import CallLogEntry

from .call_log_factory import CallLogFactory


class CallLogEntryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CallLogEntry

    call_log = factory.SubFactory(CallLogFactory)
    call_datetime = datetime.now()
    contact_type = 'indirect'
    survival_status = 'Alive'
    call_again = 'Yes'
