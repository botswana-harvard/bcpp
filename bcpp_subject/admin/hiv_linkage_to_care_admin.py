from django.contrib import admin

from edc_field_label.admin_mixin import ModifyFormLabelMixin

from ..admin_site import bcpp_subject_admin
from ..forms import HivLinkageToCareForm
from ..models import HivLinkageToCare

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HivLinkageToCare, site=bcpp_subject_admin)
class HivLinkageToCareAdmin(ModifyFormLabelMixin, CrfModelAdminMixin, admin.ModelAdmin):

    replacements = {
        'first_rep': {
            'app_model': 'bcpp_subject.hivlinkagetocare',
            'query_attr': 'subject_visit',
            'field_attr': 'kept_appt',
            'placeholder': 'last_visit_date',
            'replacement_attr': 'report_datetime',
            'attr': 'previous_visit',
        },
        'second_rep': {
            'app_model': 'bcpp_subject.hivlinkagetocare',
            'query_attr': 'appointment',
            'field_attr': 'kept_appt',
            'placeholder': 'last_appt_date',
            'replacement_attr': 'appt_datetime',
            'attr': 'previous_appt',
        },
        'third_rep': {
            'app_model': 'bcpp_subject.hivlinkagetocare',
            'query_attr': 'subject_visit',
            'field_attr': 'recommended_therapy',
            'placeholder': 'last_visit_date',
            'replacement_attr': 'report_datetime',
            'attr': 'previous_visit',
        },
        'forth_rep': {
            'app_model': 'bcpp_subject.hivlinkagetocare',
            'query_attr': 'subject_visit',
            'field_attr': 'startered_therapy',
            'placeholder': 'last_visit_date',
            'replacement_attr': 'report_datetime',
            'attr': 'previous_visit',
        },
        'fifth_rep': {
            'app_model': 'bcpp_subject.hivlinkagetocare',
            'query_attr': 'plot',
            'field_attr': 'clinic_first_date',
            'placeholder': 'community_name',
            'replacement_attr': 'community',
            'attr': 'last_community',
        },
    }

    form = HivLinkageToCareForm

    fields = (
        "subject_visit",
        "report_datetime",
        "kept_appt",
        "diff_clininc",
        "left_clininc_datetime",
        "clinic_first_datetime",
        "evidence_type_clinic",
        "evidence_type_clinic_other",
        "recommended_therapy",
        "reason_recommended",
        "reason_recommended_other",
        "startered_therapy",
        "startered_therapy_date",
        "start_therapy_clininc",
        "start_therapy_clininc_other",
        "not_refered_clininc",
        "evidence_not_refered",
        "evidence_not_refered_other",
    )
    radio_fields = {
        "kept_appt": admin.VERTICAL,
        "evidence_type_clinic": admin.VERTICAL,
        "recommended_therapy": admin.VERTICAL,
        "reason_recommended": admin.VERTICAL,
        "startered_therapy": admin.VERTICAL,
        "start_therapy_clininc": admin.VERTICAL,
        "evidence_not_refered": admin.VERTICAL}
