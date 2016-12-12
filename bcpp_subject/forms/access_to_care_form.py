from ..models import AccessToCare

from .base_subject_model_form import BaseSubjectModelForm


class AccessToCareForm (BaseSubjectModelForm):

    class Meta:
        model = AccessToCare
        fields = '__all__'
