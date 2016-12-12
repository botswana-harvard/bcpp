from edc_visit_tracking.managers import CrfModelManager

from bcpp.manager_mixins import CurrentCommunityManagerMixin


class ScheduledModelManager(CurrentCommunityManagerMixin, CrfModelManager):

    pass
