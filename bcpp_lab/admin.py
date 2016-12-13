from django.contrib import admin

from edc_base.modeladmin_mixins import ModelAdminBasicMixin

from .models import SubjectRequisition
from .admin_site import bcpp_lab_admin


@admin.register(SubjectRequisition, site=bcpp_lab_admin)
class SubjectRequisitionAdmin (ModelAdminBasicMixin, admin.ModelAdmin):

    pass
