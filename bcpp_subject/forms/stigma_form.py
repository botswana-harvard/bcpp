from ..models import Stigma, StigmaOpinion, PositiveParticipant

from .form_mixins import SubjectModelFormMixin


class StigmaForm (SubjectModelFormMixin):

    class Meta:
        model = Stigma
        fields = '__all__'


class StigmaOpinionForm (SubjectModelFormMixin):

    class Meta:
        model = StigmaOpinion
        fields = '__all__'


class PositiveParticipantForm (SubjectModelFormMixin):

    class Meta:
        model = PositiveParticipant
        fields = '__all__'
