from edc_base.model.models import ListModelMixin, BaseUuidModel


class ElectricalAppliances (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Electrical Appliances"
        verbose_name_plural = "Electrical Appliances"
