from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO

from ..choices import MONTHLY_INCOME, JOB_TYPE, REASON_UNEMPLOYED, JOB_DESCRIPTION, EDUCATION_CHOICE

from .model_mixins import CrfModelMixin


class Education (CrfModelMixin):

    """A model completed by the user on the particiapnt's level of education and work."""

    education = models.CharField(
        verbose_name="What is your highest level of education attainment?",
        max_length=65,
        choices=EDUCATION_CHOICE,
        help_text="",
    )

    working = models.CharField(
        verbose_name="Are you currently working?",
        choices=YES_NO,
        max_length=3,
        help_text="",
    )

    job_type = models.CharField(
        verbose_name="In your main job what type of work do you do?",
        max_length=45,
        choices=JOB_TYPE,
        null=True,
        blank=True,
        help_text="",
    )

    reason_unemployed = models.CharField(
        verbose_name="What is the reason why you are not working?",
        max_length=65,
        blank=True,
        null=True,
        choices=REASON_UNEMPLOYED,
        help_text="",
    )

    job_description = models.CharField(
        verbose_name="Describe the work that you do or did in your most recent"
                     " job. If you have more than one profession, choose the"
                     " one you spend the most time doing.",
        max_length=65,
        choices=JOB_DESCRIPTION,
        blank=True,
        null=True,
        help_text="",
    )

    monthly_income = models.CharField(
        verbose_name="In the past month, how much money did you earn from"
                     " work you did or received in payment [retirement benefits,"
                     " child maintenance, food basket, etc]?",
        max_length=25,
        choices=MONTHLY_INCOME,
        blank=True,
        null=True,
        help_text="",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Education"
        verbose_name_plural = "Education"
