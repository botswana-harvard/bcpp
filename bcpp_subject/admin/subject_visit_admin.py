from django.contrib import admin

from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin

from bcpp_lab.models import SubjectRequisition
from member.models import HouseholdMember

from ..admin_site import bcpp_subject_admin
from ..forms import SubjectVisitForm
from ..models import SubjectVisit


@admin.register(SubjectVisit, site=bcpp_subject_admin)
class SubjectVisitAdmin(VisitModelAdminMixin, admin.ModelAdmin):

    form = SubjectVisitForm
    visit_model_instance_field = 'subject_visit'
    requisition_model = SubjectRequisition
    dashboard_type = 'subject'

    list_display = (
        'appointment',
        'report_datetime',
        'reason',
        "info_source",
        'created',
        'user_created',
    )

    list_filter = (
        'report_datetime',
        'reason',
        'household_member__household_structure__household__plot__map_area',
        'appointment__appt_status',
        'appointment__visit_code',
    )

    search_fields = (
        'appointment__subject_identifier',
        'appointment__registered_subject__registration_identifier',
        'appointment__registered_subject__first_name',
        'appointment__registered_subject__identity',
    )

    fields = (
        'household_member',
        "appointment",
        "report_datetime",
        "comments"
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            household_members = HouseholdMember.objects.none()
            if HouseholdMember.objects.filter(id=request.GET.get('household_member', 0)):
                household_members = HouseholdMember.objects.filter(id=request.GET.get('household_member', 0))
            kwargs["queryset"] = household_members
        return super(SubjectVisitAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
