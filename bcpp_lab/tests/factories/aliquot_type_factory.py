from datetime import datetime
from lis.specimen.lab_aliquot_list.tests.factories import BaseAliquotTypeFactory

from ...models import AliquotType


class AliquotTypeFactory(BaseAliquotTypeFactory):
    FACTORY_FOR = AliquotType