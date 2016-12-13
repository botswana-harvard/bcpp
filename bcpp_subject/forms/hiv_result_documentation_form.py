from ..models import HivResultDocumentation

from .form_mixins import SubjectModelFormMixin


class HivResultDocumentationForm (SubjectModelFormMixin):

    class Meta:
        model = HivResultDocumentation
        fields = '__all__'
