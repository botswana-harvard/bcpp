from django.db import models

from edc_subset_manager.manager_mixins import SubsetManagerMixin
from edc_map.site_mappers import site_mappers


class BcppSubsetManagerMixin(SubsetManagerMixin, models.Manager):

    reference_model = 'plot.plot'
    to_reference_model = ['plot']  # e.g.  ['household_structure', 'household', 'plot']
    reference_subset_attr = 'plot_identifier'
    reference_attr = 'community'

    @property
    def reference_value(self):
        return site_mappers.current_mapper.map_area
