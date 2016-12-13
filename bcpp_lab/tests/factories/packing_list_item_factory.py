from datetime import datetime
import factory
from ...models import PackingListItem, PackingList


class PackingListItemFactory(factory.DjangoModelFactory):
    FACTORY_FOR = PackingListItem

    packing_list = factory.SubFactory(PackingList)
    item_reference = factory.Sequence(lambda n: 'item_reference{0}'.format(n))