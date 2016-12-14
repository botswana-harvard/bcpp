import factory

from datetime import datetime

from bhp066.apps.bcpp_subject.models import Circumcised


class CircumcisedFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Circumcised

    report_datetime = datetime.today()
