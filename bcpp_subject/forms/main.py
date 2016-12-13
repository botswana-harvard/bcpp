from ..models import QualityOfLife, SubstanceUse

from .form_mixins import SubjectModelFormMixin


class QualityOfLifeForm (SubjectModelFormMixin):

    class Meta:
        model = QualityOfLife
        fields = '__all__'


class SubstanceUseForm (SubjectModelFormMixin):

    class Meta:
        model = SubstanceUse
        fields = '__all__'
