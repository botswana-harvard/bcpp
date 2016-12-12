from edc_base.model.models import ListModelMixin, BaseUuidModel


class LiveWith (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Living With"
        verbose_name_plural = "Living With"
