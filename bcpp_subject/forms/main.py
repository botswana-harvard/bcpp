from ..models import QualityOfLife, SubstanceUse

from .base_subject_model_form import BaseSubjectModelForm


class QualityOfLifeForm (BaseSubjectModelForm):

    class Meta:
        model = QualityOfLife
        fields = '__all__'


class SubstanceUseForm (BaseSubjectModelForm):

    class Meta:
        model = SubstanceUse
        fields = '__all__'
