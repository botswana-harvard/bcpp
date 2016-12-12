from bhp066.apps.bcpp.base_model_form import BaseModelForm
from bhp066.apps.bcpp_list.models import (
    ElectricalAppliances, TransportMode, LiveWith,
    NeighbourhoodProblems, CircumcisionBenefits,
    FamilyPlanning, MedicalCareAccess, PartnerResidency,
    HeartDisease, Diagnoses, Religion, EthnicGroups,
    StiIllnesses, ResidentMostLikely)


class ElectricalAppliancesForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = ElectricalAppliances


class TransportModeForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = TransportMode


class LiveWithForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = LiveWith


class NeighbourhoodProblemsForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = NeighbourhoodProblems


class CircumcisionBenefitsForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = CircumcisionBenefits


class FamilyPlanningForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = FamilyPlanning


class MedicalCareAccessForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = MedicalCareAccess


class PartnerResidencyForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = PartnerResidency


class HeartDiseaseForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = HeartDisease


class DiagnosesForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = Diagnoses


class ReligionForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = Religion


class EthnicGroupsForm (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = EthnicGroups


class StiIllnesses (BaseModelForm):

    class Meta:
        model = StiIllnesses


class ResidentMostLikely (BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        return cleaned_data

    class Meta:
        model = ResidentMostLikely
