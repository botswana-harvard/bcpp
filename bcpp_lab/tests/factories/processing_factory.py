from datetime import datetime
import factory
from ...models import AliquotProcessing
from .aliquot_factory import AliquotFactory
from .profile_factory import ProfileFactory


class ProcessingFactory(factory.DjangoModelFactory):
    FACTORY_FOR = AliquotProcessing

    profile = factory.SubFactory(ProfileFactory)
    aliquot = factory.SubFactory(AliquotFactory)
