from edc_base.model.models import HistoricalRecords

from .model_mixins import CrfModelMixin, CrfModelManager, DetailedSexualHistoryMixin


class SecondPartner (DetailedSexualHistoryMixin, CrfModelMixin):

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "CS003: Second Partner"
        verbose_name_plural = "CS003: Second Partner"
