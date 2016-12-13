from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.fields import OtherCharField
from edc_constants.choices import YES_NO_REFUSED

from ..choices import (
    EMPLOYMENT_INFO, OCCUPATION, MONTHLY_INCOME, SALARY, HOUSEHOLD_INCOME, OTHER_OCCUPATION)

from .model_mixins import CrfModelMixin


class LabourMarketWages (CrfModelMixin):

    """A model completed by the user to capture information about
    the participants experience in the labour market."""

    employed = models.CharField(
        verbose_name="Are you currently employed? ",
        max_length=40,
        choices=EMPLOYMENT_INFO,
        help_text="",
    )
    occupation = models.CharField(
        verbose_name="What is your primary occupation?",
        max_length=40,
        choices=OCCUPATION,
        null=True,
        blank=True,
        help_text="main source of income.",
    )
    occupation_other = OtherCharField()

    job_description_change = models.IntegerField(
        verbose_name="In the past 3 months, how many times have you changed your job? "
                     "For example, changed your type of work or your employer. ",
        null=True,
        blank=True,
        help_text=("Note: Enter number of times. If participant does not want to answer, leave blank"),
    )

    days_worked = models.IntegerField(
        verbose_name="In the past month, how many days did you work?. ",
        null=True,
        blank=True,
        help_text="Note: Enter number of times. If participant does not want to answer, leave blank",
    )
    monthly_income = models.CharField(
        verbose_name="In the past month, what was your income? ",
        max_length=25,
        choices=MONTHLY_INCOME,
        default='None',
        null=True,
        blank=True,
        help_text="",
    )
    salary_payment = models.CharField(
        verbose_name="How were you paid for your work? ",
        max_length=20,
        choices=SALARY,
        null=True,
        blank=True,
        help_text="",
    )
    household_income = models.CharField(
        verbose_name="In the past month, what was the income of your household? ",
        max_length=25,
        null=True,
        blank=False,
        default='None',
        choices=HOUSEHOLD_INCOME,
        help_text="",
    )
    other_occupation = models.CharField(
        verbose_name="If you are not currently doing anything to earn money, then are you: ",
        max_length=45,
        choices=OTHER_OCCUPATION,
        null=True,
        blank=False,
        default='None',
        help_text="",
    )
    other_occupation_other = OtherCharField()

    govt_grant = models.CharField(
        verbose_name="Do you receive any government grant for yourself or on behalf of someone else? ",
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text="",
    )
    nights_out = models.IntegerField(
        verbose_name="In the past month, how many nights did you spend away from home?. ",
        null=True,
        blank=True,
        help_text="Note: Enter number of nights. If participant does not want to answer, leave blank",
    )
    weeks_out = models.CharField(
        verbose_name="In the last 12 months, have you spent more than 2 weeks away? ",
        max_length=17,
        choices=YES_NO_REFUSED,
        help_text="",
    )
    days_not_worked = models.IntegerField(
        verbose_name="How many days have you been prevented from working because of sickness"
                     " or visits to seek healthcare in the last 3 months. ",
        null=True,
        blank=True,
        help_text="Note: Enter number of days including zero. If participant does not want to answer,leave blank",
    )
    days_inactivite = models.IntegerField(
        verbose_name="How many days have you been prevented by illness from doing the things"
                     " you normally do (studying, housework etc.) because of sickness or visits to"
                     " seek healthcare in the last 3 months? ",
        null=True,
        blank=True,
        help_text=("Note: Enter number of days including zero. If participant "
                   "does not want to answer, leave blank"),
    )

    history = HistoricalRecords()

    def __str__(self):
        return "%s" % (self.subject_visit)

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Labour Market & Lost Wages"
        verbose_name_plural = "Labour Market & Lost Wages"
