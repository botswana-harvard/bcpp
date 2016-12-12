from django.db import models

from django.core.exceptions import ValidationError

from edc_base.model.models import HistoricalRecords
from edc_constants.constants import NOT_APPLICABLE
from edc_constants.choices import YES_NO

from ..choices import LENGTH_RESIDENCE_CHOICE, NIGHTS_AWAY_CHOICE, CATTLEPOST_LANDS_CHOICE

from .model_mixins import CrfModelMixin
from .hic_enrollment import HicEnrollment


class ResidencyMobility (CrfModelMixin):

    """A model completed by the user on the residency status of the participant."""

    length_residence = models.CharField(
        verbose_name='How long have you lived in this community?',
        max_length=25,
        choices=LENGTH_RESIDENCE_CHOICE,
        help_text="",
    )

    permanent_resident = models.CharField(
        verbose_name="In the past 12 months, have you typically spent 14 or"
                     " more nights per month in this community? ",
        max_length=10,
        choices=YES_NO,
        help_text=("If participant has moved into the "
                   "community in the past 12 months, then "
                   "since moving in has the participant typically "
                   "spent more than 14 nights per month in this community. "
                   "If 'NO (or don't want to answer)' STOP. Participant cannot be enrolled."),
    )

    intend_residency = models.CharField(
        verbose_name="Do you intend to move out of the community in the next 12 months?",
        max_length=25,
        choices=YES_NO,
        help_text="",
    )

    # see redmine 423 and 401 and 126
    nights_away = models.CharField(
        verbose_name=(
            "In the past 12 months, in total how many nights did you spend away"
            " from this community, including visits to cattle post and lands?"
            "[If you don't know exactly, give your best guess]"),
        max_length=35,
        choices=NIGHTS_AWAY_CHOICE,
        help_text="",
    )

    cattle_postlands = models.CharField(
        verbose_name=(
            "In the past 12 months, during the times you were away from this community, "
            "where were you primarily staying?"),
        max_length=25,
        choices=CATTLEPOST_LANDS_CHOICE,
        default=NOT_APPLICABLE,
        help_text="",
    )

    cattle_postlands_other = models.CharField(
        verbose_name="Give the name of the community",
        max_length=65,
        null=True,
        blank=True,
        help_text="",
    )

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.hic_enrollment_checks()
        super(ResidencyMobility, self).save(*args, **kwargs)

    def hic_enrollment_checks(self, exception_cls=None):
        exception_cls = exception_cls or ValidationError
        if HicEnrollment.objects.filter(subject_visit=self.subject_visit).exists():
            if self.permanent_resident.lower() != 'yes' or self.intend_residency.lower() != 'no':
                raise exception_cls('An HicEnrollment form exists for this subject. Values for '
                                    '\'permanent_resident\' and \'intend_residency\' cannot be changed.')

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Residency & Mobility"
        verbose_name_plural = "Residency & Mobility"
