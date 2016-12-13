from ..models import NonPregnancy

from .form_mixins import SubjectModelFormMixin


class NonPregnancyForm (SubjectModelFormMixin):

    class Meta:
        model = NonPregnancy
        fields = '__all__'
