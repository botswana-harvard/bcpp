from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..forms import RbdDemographicsForm
from ..models import RbdDemographics

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(RbdDemographics, site=bcpp_subject_admin)
class RbdDemographicsAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = RbdDemographicsForm
    fields = (
        "subject_visit",
        'religion',
        'religion_other',
        'ethnic',
        'ethnic_other',
        'marital_status',
        'num_wives',
        'husband_wives',
        'live_with',)
    radio_fields = {
        "marital_status": admin.VERTICAL, }
    filter_horizontal = ('live_with', 'religion', 'ethnic')
