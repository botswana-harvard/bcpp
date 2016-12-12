from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..filters import HivResultFilter
from ..forms import HivResultForm
from ..models import HivResult

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HivResult, site=bcpp_subject_admin)
class HivResultAdmin (CrfModelAdminMixin, admin.ModelAdmin):

    form = HivResultForm
    fields = (
        'subject_visit',
        'hiv_result',
        'hiv_result_datetime',
        'blood_draw_type',
        'insufficient_vol',
        'why_not_tested',)

    list_filter = (HivResultFilter,)

    radio_fields = {
        "hiv_result": admin.VERTICAL,
        "blood_draw_type": admin.VERTICAL,
        "insufficient_vol": admin.VERTICAL,
        'why_not_tested': admin.VERTICAL, }
