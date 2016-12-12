from edc_base.model.models import HistoricalRecords, BaseUuidModel

from .model_mixins import CrfModelMixin, CrfModelManager, DetailedSexualHistoryMixin


class ThirdPartner (DetailedSexualHistoryMixin, CrfModelMixin, BaseUuidModel):

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "CS003: Third Partner"
        verbose_name_plural = "CS003: Third Partner"
