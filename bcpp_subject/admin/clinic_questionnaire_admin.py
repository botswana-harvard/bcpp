from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..forms import ClinicQuestionnaireForm
from ..models import ClinicQuestionnaire

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(ClinicQuestionnaire, site=bcpp_subject_admin)
class ClinicQuestionnaireAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = ClinicQuestionnaireForm
    fields = (
        "subject_visit",
        "report_datetime",
        "know_hiv_status",
        "current_hiv_status",
        "on_arv",
        "arv_evidence",
    )
    radio_fields = {
        "know_hiv_status": admin.VERTICAL,
        "current_hiv_status": admin.VERTICAL,
        "on_arv": admin.VERTICAL,
        "arv_evidence": admin.VERTICAL}
