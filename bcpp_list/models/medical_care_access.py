from edc_base.model.models import ListModelMixin, BaseUuidModel


class MedicalCareAccess (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_list"
        verbose_name = "Medical Care Access"
        verbose_name_plural = "Medical Care Access"
