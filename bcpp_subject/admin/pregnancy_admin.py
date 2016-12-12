from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..models import Pregnancy
from ..forms import PregnancyForm

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Pregnancy, site=bcpp_subject_admin)
class PregnancyAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = PregnancyForm
    fields = (
        "subject_visit",
        'last_birth',
        'anc_last_pregnancy',
        'hiv_last_pregnancy',
        'preg_arv',
        'anc_reg',
        'lnmp',)
    radio_fields = {
        "anc_reg": admin.VERTICAL,
        "anc_last_pregnancy": admin.VERTICAL,
        "hiv_last_pregnancy": admin.VERTICAL,
        "preg_arv": admin.VERTICAL, }
