from ..models import TbSymptoms

from .base_subject_model_form import BaseSubjectModelForm


class TbSymptomsForm (BaseSubjectModelForm):

    class Meta:
        model = TbSymptoms
        fields = '__all__'
