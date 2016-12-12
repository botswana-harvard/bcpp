from ..models import Stigma, StigmaOpinion, PositiveParticipant

from .base_subject_model_form import BaseSubjectModelForm


class StigmaForm (BaseSubjectModelForm):

    class Meta:
        model = Stigma
        fields = '__all__'


class StigmaOpinionForm (BaseSubjectModelForm):

    class Meta:
        model = StigmaOpinion
        fields = '__all__'


class PositiveParticipantForm (BaseSubjectModelForm):

    class Meta:
        model = PositiveParticipant
        fields = '__all__'
