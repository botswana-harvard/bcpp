from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..forms import HivTestReviewForm
from ..models import HivTestReview

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HivTestReview, site=bcpp_subject_admin)
class HivTestReviewAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HivTestReviewForm
    fields = (
        "subject_visit",
        'hiv_test_date',
        'recorded_hiv_result')
    radio_fields = {
        "recorded_hiv_result": admin.VERTICAL, }
