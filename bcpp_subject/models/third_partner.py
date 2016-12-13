from edc_base.model.models import HistoricalRecords

from .model_mixins import CrfModelMixin, CrfModelManager, DetailedSexualHistoryMixin


class ThirdPartner (DetailedSexualHistoryMixin, CrfModelMixin):

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "CS003: Third Partner"
        verbose_name_plural = "CS003: Third Partner"
