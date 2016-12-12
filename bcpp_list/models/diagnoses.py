from edc_base.model.models import ListModelMixin, BaseUuidModel


class Diagnoses (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Diagnoses"
        verbose_name_plural = "Diagnoses"
