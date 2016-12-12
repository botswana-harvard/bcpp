from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..constants import ANNUAL
from ..forms import DemographicsForm
from ..models import Demographics

from .modeladmin_mixins import CrfModelAdminMixin, SubjectAdminExcludeMixin


@admin.register(Demographics, site=bcpp_subject_admin)
class DemographicsAdmin(SubjectAdminExcludeMixin, CrfModelAdminMixin, admin.ModelAdmin):

    form = DemographicsForm

    fields = [
        "subject_visit",
        'religion',
        'religion_other',
        'ethnic',
        'ethnic_other',
        'marital_status',
        'num_wives',
        'husband_wives',
        'live_with']

    custom_exclude = {
        ANNUAL:
            ['religion', 'religion_other', 'ethnic', 'ethnic_other']
    }

    radio_fields = {
        "marital_status": admin.VERTICAL, }

    filter_horizontal = ('live_with', 'religion', 'ethnic')
