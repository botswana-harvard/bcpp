from ..models import HivMedicalCare

from .base_subject_model_form import BaseSubjectModelForm


class HivMedicalCareForm (BaseSubjectModelForm):

    class Meta:
        model = HivMedicalCare
        fields = '__all__'
