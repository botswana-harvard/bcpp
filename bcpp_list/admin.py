from django.contrib import admin

from edc_base.modeladmin_mixins import ModelAdminBasicMixin

from .admin_site import bcpp_list_admin
from .models import (
    ElectricalAppliances, TransportMode, LiveWith, NeighbourhoodProblems, CircumcisionBenefits,
    FamilyPlanning, MedicalCareAccess, PartnerResidency, HeartDisease, Diagnoses, Religion,
    EthnicGroups, StiIllnesses, ResidentMostLikely)


@admin.register(ElectricalAppliances, site=bcpp_list_admin)
class ElectricalAppliancesAdmin(ModelAdminBasicMixin, admin.ModelAdmin):
    pass


@admin.register(TransportMode, site=bcpp_list_admin)
class TransportModeAdmin(ModelAdminBasicMixin, admin.ModelAdmin):
    pass


@admin.register(LiveWith, site=bcpp_list_admin)
class LiveWithAdmin(ModelAdminBasicMixin, admin.ModelAdmin):
    pass


@admin.register(NeighbourhoodProblems, site=bcpp_list_admin)
class NeighbourhoodProblemsAdmin(ModelAdminBasicMixin, admin.ModelAdmin):
    pass


@admin.register(CircumcisionBenefits, site=bcpp_list_admin)
class CircumcisionBenefitsAdmin(ModelAdminBasicMixin, admin.ModelAdmin):
    pass


@admin.register(FamilyPlanning, site=bcpp_list_admin)
class FamilyPlanningAdmin(ModelAdminBasicMixin, admin.ModelAdmin):
    pass


@admin.register(MedicalCareAccess, site=bcpp_list_admin)
class MedicalCareAccessAdmin(ModelAdminBasicMixin, admin.ModelAdmin):
    pass


@admin.register(PartnerResidency, site=bcpp_list_admin)
class PartnerResidencyAdmin(ModelAdminBasicMixin, admin.ModelAdmin):
    pass


@admin.register(HeartDisease, site=bcpp_list_admin)
class HeartDiseaseAdmin(ModelAdminBasicMixin, admin.ModelAdmin):
    pass


@admin.register(Diagnoses, site=bcpp_list_admin)
class DiagnosesAdmin(ModelAdminBasicMixin, admin.ModelAdmin):
    pass


@admin.register(Religion, site=bcpp_list_admin)
class ReligionAdmin(ModelAdminBasicMixin, admin.ModelAdmin):
    pass


@admin.register(EthnicGroups, site=bcpp_list_admin)
class EthnicGroupsAdmin(ModelAdminBasicMixin, admin.ModelAdmin):
    pass


@admin.register(StiIllnesses, site=bcpp_list_admin)
class StiIllnessesAdmin(ModelAdminBasicMixin, admin.ModelAdmin):
    pass


@admin.register(ResidentMostLikely, site=bcpp_list_admin)
class ResidentMostLikelyAdmin(ModelAdminBasicMixin, admin.ModelAdmin):
    pass
