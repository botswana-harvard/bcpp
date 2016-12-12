from django.db import models

from edc_subset_manager.manager_mixins import SubsetManagerMixin
from edc_map.site_mappers import site_mappers


class BcppSubsetManagerMixin(SubsetManagerMixin, models.Manager):

    reference_model = None  # e.g. 'bcpp_household.plot'
    reference_attr = 'community'
    to_reference_model = None  # e.g.  ['household_structure', 'household', 'plot']
    reference_subset_attr = 'plot_identifier'

    @property
    def reference_value(self):
        return site_mappers.current_mapper.map_area
