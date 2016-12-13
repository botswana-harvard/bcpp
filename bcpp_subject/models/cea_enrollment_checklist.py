from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from edc_base.model.models import HistoricalRecords
from edc_base.model.validators import datetime_not_future, eligible_if_yes
from edc_constants.choices import YES_NO, YES_NO_REFUSED

from ..choices import ENROLMENT_REASON, OPPORTUNISTIC_ILLNESSES

from .model_mixins import CrfModelMixin, CrfModelManager


class CeaEnrollmentChecklist (CrfModelMixin):

    """CE003"""

    report_datetime = models.DateTimeField(
        verbose_name="Report Date/Time",
        validators=[datetime_not_future])

    citizen = models.CharField(
        verbose_name="[Interviewer] Is the prospective participant a Botswana citizen? ",
        max_length=3,
        choices=YES_NO,
        help_text="")

    legal_marriage = models.CharField(
        verbose_name=("If not a citizen, are you legally married to a Botswana Citizen?"),
        max_length=3,
        choices=YES_NO,
        null=True,
        blank=True,
        validators=[eligible_if_yes, ],
        help_text=" if 'NO,' STOP participant cannot be enrolled")

    marriage_certificate = models.CharField(
        verbose_name=("Has the participant produced the marriage certificate, as proof? "),
        max_length=3,
        choices=YES_NO,
        null=True,
        blank=True,
        validators=[eligible_if_yes, ],
        help_text=" if 'NO,' STOP participant cannot be enrolled")

    marriage_certificate_no = models.CharField(
        verbose_name=("What is the marriage certificate number?"),
        max_length=9,
        null=True,
        blank=True,
        help_text="e.g. 000/YYYY")

    community_resident = models.CharField(
        verbose_name=("[Participant] In the past 12 months, have you typically spent 3 or"
                      " more nights per month in [name of study community]? [If moved into the"
                      " community in the past 12 months, then since moving in have you typically"
                      " spent more than 3 nights per month in this community] "),
        max_length=17,
        choices=YES_NO_REFUSED,
        validators=[eligible_if_yes, ],
        help_text="if 'NO (or don't want to answer)' STOP participant cannot be enrolled.")

    enrollment_reason = models.CharField(
        verbose_name="[Interviewer] What is the reason for enrollment of this participant? ",
        max_length=45,
        choices=ENROLMENT_REASON,
        help_text="")

    cd4_date = models.DateField(
        verbose_name="[Interviewer] Date of the most recent CD4 measurement? ",
        max_length=25,
        help_text="")

    cd4_count = models.DecimalField(
        verbose_name="[Interviewer] Most recent (within past 3 months) CD4 measurement?",
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(3000)])

    opportunistic_illness = models.CharField(
        verbose_name=("[Interviewer] Does the patient currently have AIDS opportunistic"
                      " illness (refer to SOP for list of eligible conditions)? "),
        max_length=50,
        choices=OPPORTUNISTIC_ILLNESSES,
        help_text="")

    diagnosis_date = models.DateField(
        verbose_name="[Interviewer] Date of diagnosis of the AIDS opportunistic illness? ",
        max_length=3,
        help_text="")

    date_signed = models.DateTimeField(
        verbose_name="[Interviewer] Date/ Time study CONSENT signed:",
        max_length=25,
        help_text=" if 'NO,' STOP participant cannot be enrolled")

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name = "CEA Enrollment Checklist"
        verbose_name_plural = "CEA Enrollment Checklist"
