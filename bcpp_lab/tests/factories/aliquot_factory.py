from datetime import datetime
import factory
from lis.specimen.lab_aliquot.tests.factories import BaseAliquotFactory

from ...models import Aliquot
from ..factories import ReceiveFactory, AliquotTypeFactory


class AliquotFactory(BaseAliquotFactory):
    FACTORY_FOR = Aliquot

    aliquot_type = factory.SubFactory(AliquotTypeFactory)
    receive = factory.SubFactory(ReceiveFactory)