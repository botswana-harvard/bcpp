from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..filters import Cd4ThreshHoldFilter
from ..forms import PimaForm
from ..models import Pima

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Pima, site=bcpp_subject_admin)
class PimaAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = PimaForm
    fields = (
        "subject_visit",
        'pima_today',
        'pima_today_other',
        'pima_today_other_other',
        'pima_id',
        'cd4_value',
        'cd4_datetime',
    )
    list_filter = ('subject_visit', 'cd4_datetime', 'pima_id', Cd4ThreshHoldFilter,)
    list_display = ('subject_visit', 'cd4_datetime', 'cd4_value', 'pima_id')
    radio_fields = {
        'pima_today': admin.VERTICAL,
        'pima_today_other': admin.VERTICAL}
