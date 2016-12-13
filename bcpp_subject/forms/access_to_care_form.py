from ..models import AccessToCare

from .form_mixins import SubjectModelFormMixin


class AccessToCareForm (SubjectModelFormMixin):

    class Meta:
        model = AccessToCare
        fields = '__all__'
