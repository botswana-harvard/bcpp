from datetime import datetime
import factory
from ...models import PackingList


class PackingListFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PackingList

    list_datetime = datetime.today()
    list_items = factory.Sequence(lambda n: 'list_items{0}'.format(n))
