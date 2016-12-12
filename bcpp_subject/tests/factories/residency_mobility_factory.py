import factory

from datetime import datetime

from edc_constants.constants import NOT_APPLICABLE, YES, NO

from bhp066.apps.bcpp_subject.models import ResidencyMobility


class ResidencyMobilityFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ResidencyMobility

    report_datetime = datetime.today()
    length_residence = 'Less than 6 months'
    permanent_resident = YES
    intend_residency = NO
    nights_away = 'zero'
    cattle_postlands = NOT_APPLICABLE
