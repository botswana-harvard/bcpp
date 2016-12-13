from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.validators import datetime_is_future, date_is_future
from edc_constants.constants import NOT_APPLICABLE

from ..choices import REFERRAL_CODES, REFERRAL_APPT_COMMENTS
from ..subject_referral_helper import SubjectReferralHelper

from .model_mixins import CrfModelMixin
from .tb_symptoms import TbSymptoms

REFERRAL_CLINIC_TYPES = (
    ('ANC', 'ANC'),
    ('IDCC', 'IDCC'),
    ('SMC', 'SMC'),
    ('VCT', 'VCT'),
)


class SubjectReferral(CrfModelMixin):
    """A model completed by the user to indicate a referral to care."""

    subject_referred = models.CharField(
        max_length=10,
        choices=(('Yes', 'Yes, subject has been handed a referral letter'),
                 ('No', 'No, subject has not been handed a referral letter'),
                 ('refused', 'Subject refused referral the referral letter')),
        help_text='')

    referral_appt_date = models.DateTimeField(
        verbose_name="Referral Appointment Date",
        validators=[datetime_is_future, ],
        help_text=("The calculated referral appointment date communicated to the participant. See also "
                   "attribute 'referral_appt_comment' for when the participant is unsure about attending "
                   "on this date."),
        null=True,
        editable=False
    )

    referral_clinic = models.CharField(
        max_length=50,
        editable=False,
        help_text='The full name of the current community, e.g lentsweletau.'
    )

    referral_clinic_other = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text='(not used)',
    )

    gender = models.CharField(
        max_length=10,
        null=True,
        editable=False,
        help_text='M=Male, F=Female'
    )

    citizen = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text='True if citizen, False if not, None if unknown or N/A'
    )

    citizen_spouse = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text='True if citizen_spouse, False if not, None if unknown or N/A'
    )

    hiv_result = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text=('HIV status (POS, NEG, IND) as determined by the field RA either by testing or using a combination '
                   'of verbal response and documentation. None if no result available. See also new_pos. (derived)'),
    )

    hiv_result_datetime = models.DateTimeField(
        max_length=50,
        null=True,
        editable=False,
        help_text=('HIV result datetime either from today\'s test or documentation provided by the subject or None. '
                   'See also new_pos. (derived)'),
    )

    todays_hiv_result = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text=('from HIV result of test performed by the field RA (POS, NEG, IND) or None if not performed. '
                   'The datetime of the result is hiv_result_datetime.'),
    )

    new_pos = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text="True if subject is newly diagnosed POS, false if known positive otherwise None (derived)"
    )

    last_hiv_result = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text=("Documented result from a participant's past record of HIV testing or valid documentation of "
                   "positive status (derived)")
    )

    verbal_hiv_result = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text=('from HivTestingHistory.verbal_result. HIV status as verbally provided by subject or None. See also '
                   ' if a positive result is supported by direct and indirect documentation.')
    )

    direct_hiv_documentation = models.NullBooleanField(
        null=True,
        editable=False,
        help_text=('from HivTestingHistory.has_record. True if a document was seen that confirms the subject\'s '
                   'verbally provided result, False if not, None if unknown. See also last_hiv_result.'),
    )

    indirect_hiv_documentation = models.NullBooleanField(
        null=True,
        editable=False,
        help_text=('from HivTestingHistory.other_record and from HivCareAdherence.arv_evidence. True if a document '
                   'was seen that suggests the subject is HIV positive, False if not, None if unknown.'),
    )

    last_hiv_result_date = models.DateTimeField(
        null=True,
        editable=False,
        help_text=('Recorded date of previous HIV test or of the document that provides supporting evidence of HIV '
                   'infection (derived)'),
    )

    on_art = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text=('from HivCareAdherence.on_art() method. True if subject claims to be on ARV, False if not, None if '
                   'unknown. See also art_documentation. (derived)'),
    )

    arv_documentation = models.NullBooleanField(
        null=True,
        editable=False,
        help_text=('from HivCareAdherence.arv_evidence. True if Field RA has seen documents that shows subject is on '
                   'ARV\'s, False if not, None if unknown. If True, overrides HivCareAdherence.on_arv=False'),
    )

    arv_clinic = models.CharField(
        max_length=50,
        default=None,
        null=True,
        editable=False,
        help_text="from HivCareAdherence.clinic_receiving_from. The ARV clinic where subject currently receives care"
    )

    next_arv_clinic_appointment_date = models.DateField(
        default=None,
        null=True,
        editable=False,
        help_text="from HivCareAdherence.next_appointment_date. Next appointment date at the subject's ARV clinic."
    )

    cd4_result = models.DecimalField(
        null=True,
        max_digits=6,
        decimal_places=2,
        editable=False,
        help_text='from Pima. Result of today\'s CD4 test performed in the household',
    )

    cd4_result_datetime = models.DateTimeField(
        null=True,
        editable=False,
        help_text='from Pima. datetime CD4 drawn.',
    )

    vl_sample_drawn = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text='from SubjectRequisition. True if a viral load sample was drawn in the household',
    )

    vl_sample_drawn_datetime = models.DateTimeField(
        null=True,
        editable=False,
        help_text='from SubjectRequisition. Datetime of viral load drawn.',
    )

    pregnant = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text=('from ReproductiveHealth.currently_pregnant. True if currently pregnant, False if not, None '
                   'if unknown.'),
    )

    circumcised = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text="from Circumcison.circumcised. True if circumcised, False if not, None if unknown",
    )

    part_time_resident = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text=('from eligibility checklist.part_time_resident. True if at least a part_time resident, False if '
                   'not, None if unknown')
    )

    permanent_resident = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text=('from residence and mobility.permanent_resident. True if permanent resident, False if not, None '
                   'if unknown')
    )

    tb_symptoms = models.CharField(
        max_length=100,
        null=True,
        editable=False,
        help_text=('list of symptoms from tb_symptoms. Any combination of Fever, cough, cough_blood, fever, '
                   'night_sweat, lymph_nodes, weight_loss OR None'),
    )

    urgent_referral = models.NullBooleanField(
        default=None,
        null=True,
        editable=False,
        help_text='True if one of MASA-DF, POS!-LO, POS#-LO, POS#-PR, POS!-PR, otherwise None (derived)',
    )

    referral_code = models.CharField(
        verbose_name='Referral Code',
        max_length=50,
        choices=REFERRAL_CODES,
        default='pending',
        editable=False,
        help_text="list of referral codes confirmed by the edc, comma delimited if more than one (derived)."
    )

    in_clinic_flag = models.BooleanField(
        default=False,
        editable=False,
        help_text=('system field. flag indicating participant was seen in clinic (from implementer data.) '
                   'Updated by export_transaction.'),
    )

    subject_identifier = models.CharField(
        max_length=50,
        null=True,
        editable=False,
    )

    comment = models.CharField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        help_text=('IMPORTANT: Do not include any names or other personally identifying '
                   'information in this comment')
    )

    scheduled_appt_date = models.DateField(
        verbose_name="Previously scheduled clinic appointment date in this BHS community",
        validators=[date_is_future, ],
        help_text=("Use the IDCC date. If subject is pregnant, use the ANC date instead of the IDCC date."
                   "  If the subject does not have a scheduled appointment, leave blank"),
        blank=True,
        null=True,
    )

    referral_appt_comment = models.CharField(
        verbose_name='Reason for not attending suggested appointment date',
        max_length=50,
        choices=REFERRAL_APPT_COMMENTS,
        default=NOT_APPLICABLE,
        help_text='If subject is unsure about attending the suggested appointment date, indicate the reason.'
    )

    referral_clinic_type = models.CharField(
        max_length=25,
        choices=REFERRAL_CLINIC_TYPES,
        null=True,
        editable=False,
        help_text='The clinic type of clinic the participant is referred to for services, (IDCC, VCT, ANC or SMC)'
    )

    history = HistoricalRecords()

    def __unicode__(self):
        return '{0}: {1} {2} {3}'.format(self.subject_visit,
                                         self.referral_code,
                                         self.referral_appt_date,
                                         self.referral_clinic)

    def save(self, *args, **kwargs):
        self.tb_symptoms = TbSymptoms.objects.get_symptoms(self.subject_visit)
        subject_referral_helper = SubjectReferralHelper(self)
        if subject_referral_helper.missing_data:
            raise ValidationError(('Some data is missing for the referral. '
                                   'Complete \'{0}\' first and try again.').format(
                                  subject_referral_helper.missing_data._meta.verbose_name))
        for field, value in subject_referral_helper.subject_referral_dict.iteritems():
            setattr(self, field, value)
        self.referral_code = subject_referral_helper.referral_code
        self.referral_appt_date = subject_referral_helper.referral_appt_datetime
        self.referral_clinic_type = subject_referral_helper.referral_clinic_type
        self.referral_clinic = subject_referral_helper.referral_clinic
        self.scheduled_appt_date = subject_referral_helper.original_scheduled_appt_date
        super(SubjectReferral, self).save(*args, **kwargs)

    def survey(self):
        return self.subject_visit.household_member.household_structure.survey
    survey.allow_tags = True

    def dashboard(self):
        url = reverse('subject_dashboard_url',
                      kwargs={'dashboard_type': self.subject_visit.appointment.registered_subject.subject_type.lower(),
                              'dashboard_model': 'appointment',
                              'dashboard_id': self.subject_visit.appointment.pk,
                              'show': 'appointments'})
        return """<a href="{url}" />dashboard</a>""".format(url=url)
    dashboard.allow_tags = True

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = 'Subject Referral'
        verbose_name_plural = "Subject Referral"
