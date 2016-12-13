from django.db import models

from edc_base.model.fields import OtherCharField
from edc_base.model.models import HistoricalRecords

from ..choices import COMMUNITY_ENGAGEMENT_CHOICE, VOTE_ENGAGEMENT_CHOICE, SOLVE_ENGAGEMENT_CHOICE

from .list_models import NeighbourhoodProblems
from .model_mixins import CrfModelMixin, CrfModelManager


class CommunityEngagement (CrfModelMixin):

    """A model completed by the user on the participant's engagement in the community."""

    community_engagement = models.CharField(
        verbose_name="How active are you in community activities such as"
                     " burial society, Motshelo, Syndicate, PTA, "
                     "VDC(Village Developement Committee), Mophato"
                     " and development of the community that surrounds you??",
        max_length=25,
        null=True,
        choices=COMMUNITY_ENGAGEMENT_CHOICE,
        help_text="")

    vote_engagement = models.CharField(
        verbose_name="Did you vote in the last local government election?",
        max_length=50,
        null=True,
        choices=VOTE_ENGAGEMENT_CHOICE,
        help_text="")

    problems_engagement = models.ManyToManyField(
        NeighbourhoodProblems,
        verbose_name="What are the major problems in this neighbourhood??",
        help_text=("Note:Interviewer to read question but NOT the responses. Check the boxes of"
                   " any of problems mentioned."))

    problems_engagement_other = OtherCharField(
        null=True,)

    solve_engagement = models.CharField(
        verbose_name="If there is a problem in this neighbourhood, do the"
                     " adults work together in solving it?",
        max_length=25,
        null=True,
        choices=SOLVE_ENGAGEMENT_CHOICE,
        help_text="")

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Community Engagement"
        verbose_name_plural = "Community Engagement"
