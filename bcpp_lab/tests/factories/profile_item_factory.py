from datetime import datetime
import factory
from ...models import AliquotProfileItem
from .aliquot_type_factory import AliquotTypeFactory
from .profile_factory import ProfileFactory


class ProfileItemFactory(factory.DjangoModelFactory):
    FACTORY_FOR = AliquotProfileItem

    profile = factory.SubFactory(ProfileFactory)
    aliquot_type = factory.SubFactory(AliquotTypeFactory)