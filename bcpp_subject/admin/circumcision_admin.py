from django.contrib import admin
from django.utils.translation import ugettext as _

from edc_field_label.admin_mixin import ModifyFormLabelMixin

from ..admin_site import bcpp_subject_admin
from ..constants import ANNUAL
from ..forms import CircumcisionForm, CircumcisedForm, UncircumcisedForm
from ..models import Circumcision, Circumcised, Uncircumcised

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Circumcision, site=bcpp_subject_admin)
class CircumcisionAdmin(ModifyFormLabelMixin, CrfModelAdminMixin, admin.ModelAdmin):

    replacements = {
        'first_circ_rep': {
            'field_attr': 'last_seen_circumcised',
            'placeholder': 'last_seen_circumcised',
            'replacement_attr': 'report_datetime',
            'attr': 'previous_visit',
        }
    }

    form = CircumcisionForm
    fields = (
        "subject_visit",
        'circumcised',
        'last_seen_circumcised',
        'circumcised_location',
        'circumcised_location_other',)
    radio_fields = {
        'circumcised': admin.VERTICAL,
        'last_seen_circumcised': admin.VERTICAL,
        'circumcised_location': admin.VERTICAL}
    instructions = [("Note to Interviewer: This section is to be completed "
                     "by male participants. SKIP for female participants. "),
                    _("Read to Participant: Some men are circumcised. "
                      "Male circumcision is [enter site specific word] when "
                      "the foreskin of the man's penis has been cut off. "
                      "I would like to ask you a few questions regarding "
                      "male circumcision.")]


@admin.register(Circumcised, site=bcpp_subject_admin)
class CircumcisedAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CircumcisedForm

    fields = [
        "subject_visit",
        "circumcised",
        "health_benefits_smc",
        'circ_date',
        'when_circ',
        'age_unit_circ',
        'where_circ',
        'where_circ_other',
        'why_circ',
        'why_circ_other']
    custom_exclude = {
        ANNUAL:
            ['when_circ',
             'age_unit_circ']
    }

    radio_fields = {
        "circumcised": admin.VERTICAL,
        "where_circ": admin.VERTICAL,
        "age_unit_circ": admin.VERTICAL,
        "why_circ": admin.VERTICAL, }

    filter_horizontal = ("health_benefits_smc",)


@admin.register(Uncircumcised, site=bcpp_subject_admin)
class UncircumcisedAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = UncircumcisedForm

    fields = (
        "subject_visit",
        "circumcised",
        "health_benefits_smc",
        'reason_circ',
        'reason_circ_other',
        'future_circ',
        'future_reasons_smc',
        'service_facilities',
        'aware_free',)
    radio_fields = {
        "circumcised": admin.VERTICAL,
        "reason_circ": admin.VERTICAL,
        "future_circ": admin.VERTICAL,
        "future_reasons_smc": admin.VERTICAL,
        "service_facilities": admin.VERTICAL,
        "aware_free": admin.VERTICAL}
    filter_horizontal = ("health_benefits_smc",)
