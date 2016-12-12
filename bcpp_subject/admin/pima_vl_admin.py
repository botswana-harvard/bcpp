from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..models import PimaVl
from ..forms import PimaVlForm

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(PimaVl, site=bcpp_subject_admin)
class PimaVlAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = PimaVlForm
    fields = (
        "subject_visit",
        'poc_vl_today',
        'poc_vl_today_other',
        'poc_today_vl_other_other',
        'pima_id',
        'vl_value_quatifier',
        'poc_vl_value',
        'time_of_test',
        'time_of_result',
        'easy_of_use',
        'stability',
    )
    exclude = ('poc_vl_type', 'quota_pk', 'report_datetime')
    list_filter = ('subject_visit', 'time_of_test', 'pima_id')
    list_display = ('subject_visit', 'time_of_test', 'poc_vl_value', 'pima_id', 'pre_order')
    radio_fields = {
        'poc_vl_today': admin.VERTICAL,
        'poc_vl_today_other': admin.VERTICAL,
        'vl_value_quatifier': admin.VERTICAL,
        'easy_of_use': admin.VERTICAL}
