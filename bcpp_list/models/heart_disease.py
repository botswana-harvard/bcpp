from edc_base.model.models import ListModelMixin, BaseUuidModel


class HeartDisease (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Heart Disease"
        verbose_name_plural = "Heart Disease"
