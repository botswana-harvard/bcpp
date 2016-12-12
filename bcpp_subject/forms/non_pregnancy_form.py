from ..models import NonPregnancy

from .base_subject_model_form import BaseSubjectModelForm


class NonPregnancyForm (BaseSubjectModelForm):

    class Meta:
        model = NonPregnancy
        fields = '__all__'
