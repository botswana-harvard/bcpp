from ..models import TbSymptoms

from .form_mixins import SubjectModelFormMixin


class TbSymptomsForm (SubjectModelFormMixin):

    class Meta:
        model = TbSymptoms
        fields = '__all__'
