from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.fields import OtherCharField
from edc_constants.choices import YES_NO_NA, NOT_APPLICABLE, YES_NO, YES_NO_UNSURE

from .list_models import FamilyPlanning
from .model_mixins import CrfModelMixin


class ReproductiveHealth (CrfModelMixin):

    """A model completed by the user on the participant's reproductive health."""

    number_children = models.IntegerField(
        verbose_name="How many children have you given birth to? Please include any"
                     " children that may have died at (stillbirth) or after birth. "
                     "Do not include any current pregnancies or miscarriages that occur"
                     " early in pregnancy (prior to 20 weeks).",
        default=0,
        help_text="",
    )

    menopause = models.CharField(
        verbose_name="Have you reached menopause (more than 12 months without a period)?",
        max_length=3,
        choices=YES_NO,
        help_text="this also refers to pre-menopause",
    )

    family_planning = models.ManyToManyField(
        FamilyPlanning,
        verbose_name="In the past 12 months, have you used any methods to prevent"
                     " pregnancy ?",
        blank=True,
        help_text="check all that apply",
    )

    family_planning_other = OtherCharField()

    currently_pregnant = models.CharField(
        verbose_name="Are you currently pregnant?",
        null=True,
        blank=True,
        max_length=25,
        choices=YES_NO_UNSURE,
        help_text="",
    )

    when_pregnant = models.CharField(
        verbose_name="Did you become pregnant since the last interview we had with you?",
        max_length=3,
        choices=YES_NO,
        help_text="",
    )

    gestational_weeks = models.IntegerField(
        verbose_name="At about what gestational age (in weeks) did you start arv's during "
        "this (or your last) pregnancy?",
        null=True,
        blank=True,
        help_text="gestational age in WEEKS. Among HIV-infected women who took/started ARVs during their last"
        " (or current pregnancy).",
    )

    pregnancy_hiv_tested = models.CharField(
        verbose_name="Were you tested for HIV during your most recent (or this current) pregnancy?",
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        max_length=3,
        help_text="Among women who were not known to be HIV-infected prior to the last (or current pregnancy).",
    )

    pregnancy_hiv_retested = models.CharField(
        verbose_name="If you tested HIV-negative during the most recent (or this current) pregnancy, were you"
        " re-tested for HIV in the last 3 months of your pregnancy or at delivery? ",
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        max_length=3,
        help_text="if the respondent has reached that point by the time of the current interview.",
    )

    history = HistoricalRecords()

    def validate_not_hiv_infected(self, enrollment_checklist, household_member, exception_cls=None):
        pass

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Reproductive Health"
        verbose_name_plural = "Reproductive Health"
