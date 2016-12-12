from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..forms import OutpatientCareForm
from ..models import OutpatientCare

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(OutpatientCare, site=bcpp_subject_admin)
class OutpatientCareAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = OutpatientCareForm
    fields = (
        "subject_visit",
        "govt_health_care",
        "dept_care",
        "prvt_care",
        "trad_care",
        "care_visits",
        "facility_visited",
        "specific_clinic",
        "care_reason",
        "care_reason_other",
        "outpatient_expense",
        "travel_time",
        "transport_expense",
        "cost_cover",
        "waiting_hours",
    )
    radio_fields = {
        "govt_health_care": admin.VERTICAL,
        "dept_care": admin.VERTICAL,
        "prvt_care": admin.VERTICAL,
        "trad_care": admin.VERTICAL,
        "facility_visited": admin.VERTICAL,
        "care_reason": admin.VERTICAL,
        "travel_time": admin.VERTICAL,
        "cost_cover": admin.VERTICAL,
        "waiting_hours": admin.VERTICAL,
    }
