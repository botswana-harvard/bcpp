from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..constants import ANNUAL
from ..forms import HivTestedForm
from ..models import HivTested

from .modeladmin_mixins import CrfModelAdminMixin, SubjectAdminExcludeMixin


@admin.register(HivTested, site=bcpp_subject_admin)
class HivTestedAdmin(SubjectAdminExcludeMixin, CrfModelAdminMixin, admin.ModelAdmin):

    form = HivTestedForm
    fields = [
        "subject_visit",
        'num_hiv_tests',
        'where_hiv_test',
        'where_hiv_test_other',
        'why_hiv_test',
        'hiv_pills',
        'arvs_hiv_test']
    custom_exclude = {ANNUAL: [
        'num_hiv_tests', 'hiv_pills', 'arvs_hiv_test', 'why_hiv_test']
    }

    radio_fields = {
        "where_hiv_test": admin.VERTICAL,
        "why_hiv_test": admin.VERTICAL,
        "hiv_pills": admin.VERTICAL,
        "arvs_hiv_test": admin.VERTICAL, }
