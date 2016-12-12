from edc_base.model.models import ListModelMixin, BaseUuidModel


class Religion (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Religion"
        verbose_name_plural = "Religion"
