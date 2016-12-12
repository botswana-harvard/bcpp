from edc_base.model.models import ListModelMixin, BaseUuidModel


class CircumcisionBenefits (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Circumcision Benefits"
        verbose_name_plural = "Circumcision Benefits"
