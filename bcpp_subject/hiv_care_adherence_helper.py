from django.contrib import admin

from edc.subject.appointment.models import Appointment
from edc_constants.constants import POS

from ..models import SubjectVisit

from .subject_status_helper import SubjectStatusHelper


class HivCareAdherenceHelper(object):

    baseline_fields = [
        "subject_visit",
        "first_positive",
        "medical_care",
        "no_medical_care",
        "no_medical_care_other",
        'ever_recommended_arv',
        'ever_taken_arv',
        'why_no_arv',
        'why_no_arv_other',
        'first_arv',
        'on_arv',
        'arv_evidence',
        'clinic_receiving_from',
        'next_appointment_date',
        'arv_stop_date',
        'arv_stop',
        'arv_stop_other',
        'adherence_4_day',
        'adherence_4_wk']

    annual_radio_fields = {
        "arv_stop": admin.VERTICAL,
        "adherence_4_day": admin.VERTICAL,
        "adherence_4_wk": admin.VERTICAL,
        "arv_evidence": admin.VERTICAL}

    def __init__(self, visit_instance):
        self.visit_instance = visit_instance

    @property
    def annual_radio_fields_pos_and_art(self):
        subject_helper = SubjectStatusHelper(self.func_baseline_visit_instance)
        if subject_helper.hiv_result == POS and subject_helper.on_art:
            return self.annual_radio_fields

    @property
    def annual_fields_pos_and_art(self):
        """ Known Positive from T0 and on ART """
        subject_helper = SubjectStatusHelper(self.func_baseline_visit_instance)
        if subject_helper.hiv_result == POS and subject_helper.on_art:
            return [f for f in self.baseline_fields if f not in ["first_positive",
                                                                 "medical_care", "no_medical_care",
                                                                 "ever_recommended_arv", "ever_taken_arv",
                                                                 "why_no_arv", "on_arv"]]

    @property
    def func_baseline_visit_instance(self):
        """ Returns subject_visit for T0 """
        registered_subject = self.visit_instance.appointment.registered_subject
        baseline_appointment = Appointment.objects.filter(
            registered_subject=registered_subject, visit_definition__code='T0')[0]
        return SubjectVisit.objects.get(
            household_member__registered_subject=registered_subject, appointment=baseline_appointment)
