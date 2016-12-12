from edc_base.model.models import ListModelMixin, BaseUuidModel


class TransportMode (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Transport Mode"
        verbose_name_plural = "Transport Mode"
