from datetime import datetime
import factory
from ...models import AliquotProfile
from .aliquot_type_factory import AliquotTypeFactory


class ProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = AliquotProfile

    aliquot_type = factory.SubFactory(AliquotTypeFactory)
    name = factory.Sequence(lambda n: 'name{0}'.format(n))