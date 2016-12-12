from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..forms import HivUntestedForm
from ..models import HivUntested

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HivUntested, site=bcpp_subject_admin)
class HivUntestedAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HivUntestedForm
    fields = (
        "subject_visit",
        'why_no_hiv_test',
        'hiv_pills',
        'arvs_hiv_test',)
    radio_fields = {
        "why_no_hiv_test": admin.VERTICAL,
        "hiv_pills": admin.VERTICAL,
        "arvs_hiv_test": admin.VERTICAL, }
