from copy import copy
from collections import namedtuple

from django.apps import apps as django_apps

from edc_map.site_mappers import site_mappers
from edc_constants.constants import POS, NEG
from member.models import EnrollmentChecklist

from .choices import REFERRAL_CODES
from .constants import ANNUAL_CODES, BASELINE_CODES, BASELINE, ANNUAL
from .models import (
    SubjectConsent, ResidencyMobility, Circumcision, ReproductiveHealth, SubjectLocator, HivCareAdherence)
from .utils import convert_to_nullboolean

from .subject_status_helper import SubjectStatusHelper
from .subject_referral_appt_helper import SubjectReferralApptHelper


class SubjectReferralHelper(object):
    """A class that calculates the referral code or returns a blank string.

    See property :func:`referral_code`"""

    def __init__(self, subject_referral=None):
        self._circumcised = None
        self._enrollment_checklist_instance = None
        self._pregnant = None
        self._referral_clinic = None
        self._referral_code = None
        self._referral_code_list = []
        self._subject_consent_instance = None
        self._subject_referral = None
        self._subject_referral_dict = {}
        self._subject_status_helper = None
        self.community_code = site_mappers.get_mapper(site_mappers.current_map_area).map_code
        # self.models dict is also used in the signal
        self.models = copy(SubjectStatusHelper.models)
        self.models[BASELINE].update({
            'subject_locator': SubjectLocator,
            'circumcision': Circumcision,
            'reproductive_health': ReproductiveHealth,
            'residency_mobility': ResidencyMobility,
            'subject_consent': SubjectConsent,
        })
        self.models[ANNUAL].update({
            'subject_locator': SubjectLocator,
            'circumcision': Circumcision,
            'reproductive_health': ReproductiveHealth,
            'residency_mobility': ResidencyMobility,
            'subject_consent': SubjectConsent,
        })
        self.models[BASELINE].update({'subject_requisition': django_apps.get_model('bcpp_lab', 'SubjectRequisition')})
        self.models[ANNUAL].update({'subject_requisition': django_apps.get_model('bcpp_lab', 'SubjectRequisition')})
        self.previous_subject_referrals = []
        if subject_referral:
            self.subject_referral = subject_referral

    def __repr__(self):
        return 'SubjectStatusHelper({0.subject_referral!r})'.format(self)

    def __str__(self):
        return '({0.subject_referral!r})'.format(self)

    @property
    def timepoint_key(self):
        """Returns a dictionary key of either baseline or annual base in the visit code."""
        if self.subject_referral.subject_visit.appointment.visit_definition.code in BASELINE_CODES:
            return BASELINE
        return ANNUAL

    @property
    def subject_referral(self):
        return self._subject_referral

    @subject_referral.setter
    def subject_referral(self, subject_referral):
        SubjectReferral = django_apps.get_model('bcpp_subject', 'SubjectReferral')
        if self._subject_referral:
            # reset every attribute
            self._subject_referral = None
            self.__init__()
        self._subject_referral = subject_referral
        # prepare a queryset of visits previous to visit_instance
        internal_identifier = subject_referral.subject_visit.household_member.internal_identifier
        self.previous_subject_referrals = SubjectReferral.objects.filter(
            subject_visit__household_member__internal_identifier=internal_identifier,
            report_datetime__lt=subject_referral.report_datetime).order_by('report_datetime')

    @property
    def subject_status_helper(self):
        if not self._subject_status_helper:
            self._subject_status_helper = SubjectStatusHelper(copy(self.subject_visit))
        return self._subject_status_helper

    @property
    def gender(self):
        return self.subject_referral.subject_visit.appointment.registered_subject.gender

    @property
    def household_member(self):
        return self.subject_referral.subject_visit.household_member

    @property
    def subject_identifier(self):
        return self.subject_referral.subject_visit.appointment.registered_subject.subject_identifier

    @property
    def subject_visit(self):
        return self.subject_referral.subject_visit

    def visit_code(self):
        return self.subject_referral.subject_visit.appointment.visit_definition.code

    @property
    def survey(self):
        return self.subject_referral.subject_visit.household_member.household_structure.survey

    @property
    def hiv_result(self):
        return self.subject_status_helper.hiv_result

    @property
    def hiv_care_adherence_next_appointment(self):
        """Return the next appoint date from the HIV care and adherence."""
        try:
            hiv_care_adherence = HivCareAdherence.objects.get(subject_visit=self.subject_visit)
            next_appointment_date = hiv_care_adherence.next_appointment_date
        except HivCareAdherence.DoesNotExist:
            next_appointment_date = None
        return next_appointment_date

    @property
    def on_art(self):
        """Returns None if hiv_result==NEG otherwise True if hiv_result==POS and on ART or False if not."""
        return self.subject_status_helper.on_art

    @property
    def subject_referral_dict(self):
        """Returns a dictionary of the attributes {name: value, ...}
        from this class that match, by name, field attributes in the
        SubjectReferral model."""
        if not self._subject_referral_dict:
            self._subject_referral_dict = {}
            for attr in self.subject_referral.__dict__:
                if attr in dir(self) and not attr.startswith('_'):
                    self._subject_referral_dict.update({attr: getattr(self, attr)})
            self._subject_referral_dict.update({'subject_identifier': getattr(self, 'subject_identifier')})
        return self._subject_referral_dict

    @property
    def subject_referral_tuple(self):
        """Returns a dictionary of the attributes {name: value, ...}
        from this class that match, by name, field attributes in the
        SubjectReferral model."""
        Tpl = namedtuple('SubjectReferralTuple', 'subject_visit ' + '  '.join(self.subject_referral.keys()))
        self._subject_referral_tuple = Tpl(self.subject_visit, *self.subject_referral.values())
        return self._subject_referral_tuple

    def male_refferal_code(self):
        """ docstring is required"""
        if self.circumcised:
            self._referral_code_list.append('TST-HIV')  # refer if status unknown
        else:
            if self.circumcised is False:
                self._referral_code_list.append('SMC-UNK')  # refer if status unknown
            else:
                self._referral_code_list.append('SMC?UNK')  # refer if status unknown

    def refferal_code_neg(self):
        if self.gender == 'F' and self.pregnant:  # only refer F if pregnant
            self._referral_code_list.append('NEG!-PR')
        elif self.gender == 'M' and self.circumcised is False:  # only refer M if not circumcised
            self._referral_code_list.append('SMC-NEG')
        elif self.gender == 'M' and self.circumcised is None:  # only refer M if not circumcised
            self._referral_code_list.append('SMC?NEG')

    def refferal_code_pos_not_on_art(self):
        if not self.cd4_result:
            self._referral_code_list.append('TST-CD4')
        elif self.cd4_result > (500 if self.intervention else 350):
            self._referral_code_list.append(
                'POS!-HI') if self.new_pos else self._referral_code_list.append('POS#-HI')
        elif self.cd4_result <= (500 if self.intervention else 350):
            self._referral_code_list.append(
                'POS!-LO') if self.new_pos else self._referral_code_list.append('POS#-LO')

    def refferal_code_pos_on_art(self):
        """ Docstring is required"""
        self._referral_code_list.append('MASA-CC')
        if self.defaulter:
            self._referral_code_list = [
                'MASA-DF' for item in self._referral_code_list if item == 'MASA-CC']
        if self.pregnant:
            self._referral_code_list = [
                'POS#-AN' for item in self._referral_code_list if item == 'MASA-CC']
        if self.visit_code in ANNUAL_CODES:  # do not refer to MASA-CC except if BASELINE
            try:
                self._referral_code_list.remove('MASA-CC')
            except ValueError:
                pass

    def refferal_code_pos(self):
        """ Docstring is required"""
        if self.gender == 'F' and self.pregnant and self.on_art:
            self._referral_code_list.append('POS#-AN')
        elif self.gender == 'F' and self.pregnant and not self.on_art:
            self._referral_code_list.append(
                'POS!-PR') if self.new_pos else self._referral_code_list.append('POS#-PR')
        elif not self.on_art:
            self.refferal_code_pos_not_on_art()
        elif self.on_art:
            self.refferal_code_pos_on_art()

    def refferal_code_list_with_hiv_result(self):
        if self.hiv_result == 'IND':
            # do not set referral_code_list to IND
            pass
        elif self.hiv_result == NEG:
            self.refferal_code_neg()
        elif self.hiv_result == POS:
            self.refferal_code_pos()
        else:
            self._referral_code_list.append('TST-HIV')

    @property
    def referral_code_list(self):
        """Returns a list of referral codes by reviewing the conditions for referral."""
        if not self._referral_code_list:
            is_declined = None
            try:
                is_declined = True if self.hiv_result == "Declined" else False
            except AttributeError:
                pass
            if not self.hiv_result or is_declined:
                if self.gender == 'M':
                    self.male_refferal_code()
                elif self.pregnant:
                    self._referral_code_list.append('UNK?-PR')
                else:
                    self._referral_code_list.append('TST-HIV')
            else:
                self.refferal_code_list_with_hiv_result()
            # refer if on art and known positive to get VL, and o get outsiders to transfer care
            # referal date is the next appointment date if on art
            if self._referral_code_list:
                self._referral_code_list = list(set((self._referral_code_list)))
                self._referral_code_list.sort()
                for code in self._referral_code_list:
                    if code not in self.valid_referral_codes:
                        raise ValueError('{0} is not a valid referral code.'.format(code))
        return self._referral_code_list

    @property
    def referral_code(self):
        """Returns a string of referral codes as a join of the
        list of referral codes delimited by ","."""
        if self._referral_code is None:
            self._referral_code = ','.join(self.referral_code_list)
            self._referral_code = self.remove_smc_in_annual_ecc(self._referral_code)
        return self._referral_code

    def remove_smc_in_annual_ecc(self, referral_code):
        """Removes any SMC referral codes if in the ECC during an ANNUAL survey."""
        survey_slug = self.subject_visit.household_member.household_structure.survey.survey_slug
        code = referral_code.replace('SMC-NEG', '').replace('SMC?NEG', '').replace('SMC-UNK', '').replace('SMC?UNK', '')
        if (not self.intervention and survey_slug != 'bcpp-year-1'):
            referral_code = code
        return referral_code

    @property
    def valid_referral_codes(self):
        return [code for code, _ in REFERRAL_CODES if not code == 'pending']

    @property
    def intervention(self):
        return site_mappers.get_mapper(site_mappers.current_map_area).intervention

    @property
    def arv_clinic(self):
        try:
            clinic_receiving_from = self._subject_status_helper.hiv_care_adherence_instance.clinic_receiving_from
        except AttributeError:
            clinic_receiving_from = None
        return clinic_receiving_from

    @property
    def circumcised(self):
        """Returns None if female otherwise True if circumcised or False if not."""
        if self._circumcised is None:
            if self.gender == 'M':
                circumcised = None
                if self.previous_subject_referrals:
                    # save current visit
                    previous_subject_referrals = copy(self.previous_subject_referrals)
                    for subject_referral in previous_subject_referrals:
                        # check for CIRCUMCISED result from previous data
                        circumcised = subject_referral.circumcised
                        if circumcised:
                            break
                if not circumcised:
                    try:
                        circumcision_instance = self.models[self.timepoint_key].get(
                            'circumcision').objects.get(subject_visit=self.subject_visit)
                        circumcised = convert_to_nullboolean(circumcision_instance.circumcised)
                    except self.models[self.timepoint_key].get('circumcision').DoesNotExist:
                        circumcised = None
                self._circumcised = circumcised
        return self._circumcised

    @property
    def citizen(self):
        citizen = None
        try:
            citizen = (self.enrollment_checklist_instance.citizen == 'Yes' and
                       self.subject_consent_instance.identity is not None)
        except AttributeError:
            citizen = None
        return citizen

    @property
    def citizen_spouse(self):
        citizen_spouse = None
        try:
            citizen_spouse = (self.enrollment_checklist_instance.legal_marriage == 'Yes' and
                              self.subject_consent_instance.identity is not None)
        except AttributeError:
            citizen_spouse = None
        return citizen_spouse

    @property
    def next_arv_clinic_appointment_date(self):
        next_appointment_date = None
        try:
            next_appointment_date = self._subject_status_helper.hiv_care_adherence_instance.next_appointment_date
        except AttributeError:
            pass
        return next_appointment_date

    @property
    def part_time_resident(self):
        """Returns True if part_time_resident as stated on enrollment_checklist."""
        try:
            # Note: Reading the question in EnrollmentChecklist, you should interpret in the following way,
            # Yes => not part_time_resident, No => part_time_resident.
            part_time_resident = not convert_to_nullboolean(self.enrollment_checklist_instance.part_time_resident)
        except AttributeError:
            part_time_resident = None
        return part_time_resident

    @property
    def permanent_resident(self):
        """Returns True if permanent resident as stated on ResidencyMobility."""
        try:
            residency_mobility_instance = self.models[self.timepoint_key].get('residency_mobility').objects.get(
                subject_visit=self.subject_visit)
            permanent_resident = convert_to_nullboolean(residency_mobility_instance.permanent_resident)
        except self.models[self.timepoint_key].get('residency_mobility').DoesNotExist:
            permanent_resident = None
        return permanent_resident

    @property
    def pregnant(self):
        """Returns None if male otherwise True if pregnant or False if not."""
        if self.gender == 'F':
            if not self._pregnant:
                try:
                    reproductive_health = self.models[self.timepoint_key].get('reproductive_health').objects.get(
                        subject_visit=self.subject_visit)
                    self._pregnant = convert_to_nullboolean(reproductive_health.currently_pregnant)
                except self.models[self.timepoint_key].get('reproductive_health').DoesNotExist:
                    self._pregnant = None
        return self._pregnant

    @property
    def tb_symptoms(self):
        """Returns the tb_symptoms list as a convenience.

        Not necessary for determining the referral code."""
        return self.subject_referral.tb_symptoms

    @property
    def urgent_referral(self):
        """Compares the referral_codes to the "urgent" referrals
        list and sets to true on a match."""
        URGENT_REFERRALS = ['MASA-DF', 'POS!-LO', 'POS#-LO', 'POS!-HI', 'POS#-HI', 'POS#-PR', 'POS!-PR']
        return True if [code for code in self.referral_code_list if code in URGENT_REFERRALS] else False

    @property
    def enrollment_checklist_instance(self):
        # Can have multiple enrollment checklists for one each household_member__internal_identifier,
        # but only one of them will be associated with a consented member. Thats the 1 we want to pull here.
        if not self._enrollment_checklist_instance:
            self._enrollment_checklist_instance = EnrollmentChecklist.objects.get(
                household_member__internal_identifier=self.subject_visit.household_member.internal_identifier,
                household_member__is_consented=True)
        return self._enrollment_checklist_instance

    @property
    def subject_consent_instance(self):
        if not self._subject_consent_instance:
            self._subject_consent_instance = self.subject_referral.CONSENT_MODEL.consent.valid_consent_for_period(
                self.subject_identifier, self.subject_referral.report_datetime)
        return self._subject_consent_instance

    @property
    def subject_referral_appt_helper(self):
        return SubjectReferralApptHelper(
            self.referral_code,
            base_date=self.subject_referral.report_datetime,
            scheduled_appt_date=self.subject_referral.scheduled_appt_date,
            hiv_care_adherence_next_appointment=self.hiv_care_adherence_next_appointment
        )

    @property
    def referral_appt_datetime(self):
        return self.subject_referral_appt_helper.referral_appt_datetime

    @property
    def referral_clinic_type(self):
        return self.subject_referral_appt_helper.referral_clinic_type

    @property
    def referral_clinic(self):
        return self.subject_referral_appt_helper.community_name

    @property
    def original_scheduled_appt_date(self):
        return self.subject_referral_appt_helper.original_scheduled_appt_date

    @property
    def new_pos(self):
        return self.subject_status_helper.new_pos

    @property
    def todays_hiv_result(self):
        return self.subject_status_helper.todays_hiv_result

    @property
    def hiv_result_datetime(self):
        return self.subject_status_helper.hiv_result_datetime

    @property
    def last_hiv_result_date(self):
        return self.subject_status_helper.last_hiv_result_date

    @property
    def verbal_hiv_result(self):
        return self.subject_status_helper.verbal_hiv_result

    @property
    def last_hiv_result(self):
        return self.subject_status_helper.last_hiv_result

    @property
    def indirect_hiv_documentation(self):
        return self.subject_status_helper.indirect_hiv_documentation

    @property
    def direct_hiv_documentation(self):
        return self.subject_status_helper.direct_hiv_documentation

    @property
    def defaulter(self):
        return self.subject_status_helper.defaulter

    @property
    def cd4_result(self):
        return self.subject_status_helper.cd4_result

    @property
    def vl_sample_drawn(self):
        return self.subject_status_helper.vl_sample_drawn

    @property
    def vl_sample_drawn_datetime(self):
        return self.subject_status_helper.vl_sample_drawn_datetime

    @property
    def arv_documentation(self):
        return self.subject_status_helper.arv_documentation

    @property
    def cd4_result_datetime(self):
        return self.subject_status_helper.cd4_result_datetime
