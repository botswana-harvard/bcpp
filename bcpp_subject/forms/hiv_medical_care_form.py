from ..models import HivMedicalCare

from .form_mixins import SubjectModelFormMixin


class HivMedicalCareForm (SubjectModelFormMixin):

    class Meta:
        model = HivMedicalCare
        fields = '__all__'
