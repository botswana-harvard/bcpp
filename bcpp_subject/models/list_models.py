from edc_base.model.models import ListModelMixin, BaseUuidModel


class CircumcisionBenefits (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Circumcision Benefits"
        verbose_name_plural = "Circumcision Benefits"


class Diagnoses (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Diagnoses"
        verbose_name_plural = "Diagnoses"


class EthnicGroups (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Ethnic Groups"
        verbose_name_plural = "Ethnic Groups"


class FamilyPlanning (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Family Planning"
        verbose_name_plural = "Family Planning"


class HeartDisease (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Heart Disease"
        verbose_name_plural = "Heart Disease"


class LiveWith (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Living With"
        verbose_name_plural = "Living With"


class MedicalCareAccess (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Medical Care Access"
        verbose_name_plural = "Medical Care Access"


class NeighbourhoodProblems (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Neighbourhood Problems"
        verbose_name_plural = "Neighbourhood Problems"


class PartnerResidency (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Partner Residency"
        verbose_name_plural = "Partner Residency"


class Religion (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Religion"
        verbose_name_plural = "Religion"


class ResidentMostLikely (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Resident Most Likely Status"
        verbose_name_plural = "Resident Most Likely Status"


class StiIllnesses (ListModelMixin, BaseUuidModel):

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "HIV-related illness"
        verbose_name_plural = "HIV-related illness"
