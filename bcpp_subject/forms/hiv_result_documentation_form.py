from ..models import HivResultDocumentation

from .base_subject_model_form import BaseSubjectModelForm


class HivResultDocumentationForm (BaseSubjectModelForm):

    class Meta:
        model = HivResultDocumentation
        fields = '__all__'
