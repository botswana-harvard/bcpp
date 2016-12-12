from django.db import models

from edc_base.model.models import HistoricalRecords

from ..choices import AGREE_STRONGLY

from .model_mixins import CrfModelMixin


class PositiveParticipant (CrfModelMixin):

    """A model completed by the user to help understand some challenges of being HIV positive."""

    internalize_stigma = models.CharField(
        verbose_name="I think less of myself.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    internalized_stigma = models.CharField(
        verbose_name="I have felt ashamed because of having HIV.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    friend_stigma = models.CharField(
        verbose_name="I fear that if I disclosed my HIV status to my"
                     " friends, they would lose respect for me.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    family_stigma = models.CharField(
        verbose_name="I fear that if I disclosed my HIV status to my family,"
                     " they would exclude me from usual family activities.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    enacted_talk_stigma = models.CharField(
        verbose_name="People have talked badly about me.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    enacted_respect_stigma = models.CharField(
        verbose_name="I have lost respect or standing in the community.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    enacted_jobs_tigma = models.CharField(
        verbose_name="I have lost a job because of having HIV.",
        max_length=25,
        null=True,
        choices=AGREE_STRONGLY,
        help_text="",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Positive Participant"
        verbose_name_plural = "Positive Participant"
