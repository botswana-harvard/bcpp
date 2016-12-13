from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO_DWTA

from ..choices import ALCOHOL_SEX

from .model_mixins import CrfModelMixin, CrfModelManager


class SexualBehaviour (CrfModelMixin):

    """A model completed by the user on the participant's sexual behaviour."""

    ever_sex = models.CharField(
        verbose_name="In your lifetime, have you ever had sex with anyone"
                     " (including your spouse, friends, or someone you have just met)?",
        max_length=25,
        choices=YES_NO_DWTA,
        help_text="",
    )

    lifetime_sex_partners = models.IntegerField(
        verbose_name="In your lifetime, how many different people have you had"
                     " sex with?  Please remember to include casual and once-off partners"
                     " (prostitutes and truck drivers) as well as long-term partners"
                     " (spouses, boyfriends/girlfriends)[If you can't recall the exact "
                     "number, please give a best guess]",
        null=True,
        blank=True,
        help_text="",
    )

    last_year_partners = models.IntegerField(
        verbose_name="In the past 12 months, how many different people have you had"
                     " sex with?  Please remember to include casual and once-off partners"
                     " (prostitutes and truck drivers) as well as long-term partners"
                     " (spouses, boyfriends/girlfriends)[If you can't recall the exact "
                     "number, please give a best guess]",
        null=True,
        blank=True,
        help_text="Note:Leave blank if participant does not want to respond. ",
    )

    more_sex = models.CharField(
        verbose_name="In the past 12 months, did you have sex with somebody"
                     " living outside of the community?",
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
        help_text="",
    )

    first_sex = models.IntegerField(
        verbose_name="How old were you when you had sex for the first time?"
                     " [If you can't recall the exact age, please give a best guess]",
        null=True,
        blank=True,
        validators=[MinValueValidator(10), MaxValueValidator(64)],
        help_text="Note:leave blank if participant does not want to respond.",
    )

    condom = models.CharField(
        verbose_name="During the last [most recent] time you had sex, did"
                     " you or your partner use a condom?",
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
        help_text="",
    )

    alcohol_sex = models.CharField(
        verbose_name="During the last [most recent] time you had sex, were"
                     " you or your partner drinking alcohol?",
        max_length=25,
        null=True,
        blank=True,
        choices=ALCOHOL_SEX,
        help_text="",
    )

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Sexual Behaviour"
        verbose_name_plural = "Sexual Behaviour"
