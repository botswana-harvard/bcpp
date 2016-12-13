from datetime import datetime
from lis.specimen.lab_panel.tests.factories import BasePanelFactory

from ...models import Panel


class PanelFactory(BasePanelFactory):
    FACTORY_FOR = Panel