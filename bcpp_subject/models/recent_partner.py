from edc_base.model.models import HistoricalRecords

from .model_mixins import CrfModelMixin, DetailedSexualHistoryMixin


class MostRecentPartner (DetailedSexualHistoryMixin, CrfModelMixin):

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "CS003: Most Recent Partner"
        verbose_name_plural = "CS003: Most Recent Partner"
