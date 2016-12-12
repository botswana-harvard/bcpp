from collections import OrderedDict

from django.contrib import admin

from edc_locator.modeladmin_mixins import ModelAdminLocatorMixin

from ..actions import export_locator_for_cdc_action
from ..admin_site import bcpp_subject_admin
from ..filters import SubjectLocatorIsReferredListFilter, SubjectCommunityListFilter
from ..forms import SubjectLocatorForm
from ..models import SubjectLocator

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SubjectLocator, site=bcpp_subject_admin)
class SubjectLocatorAdmin(ModelAdminLocatorMixin, CrfModelAdminMixin, admin.ModelAdmin):

    form = SubjectLocatorForm
    fields = (
        'subject_visit',
        'date_signed',
        'mail_address',
        'home_visit_permission',
        'physical_address',
        'may_follow_up',
        'may_sms_follow_up',
        'subject_cell',
        'subject_cell_alt',
        'subject_phone',
        'subject_phone_alt',
        'may_contact_someone',
        'contact_name',
        'contact_rel',
        'contact_physical_address',
        'contact_cell',
        'alt_contact_cell_number',
        'contact_phone',
        'has_alt_contact',
        'alt_contact_name',
        'alt_contact_rel',
        'alt_contact_cell',
        'other_alt_contact_cell',
        'alt_contact_tel',
        'may_call_work',
        'subject_work_place',
        'subject_work_phone',)
    radio_fields = {
        "home_visit_permission": admin.VERTICAL,
        "may_follow_up": admin.VERTICAL,
        "may_sms_follow_up": admin.VERTICAL,
        "has_alt_contact": admin.VERTICAL,
        "may_call_work": admin.VERTICAL,
        "may_contact_someone": admin.VERTICAL, }
    list_filter = (
        SubjectLocatorIsReferredListFilter,
        SubjectCommunityListFilter,
        'may_follow_up',
        'may_contact_someone',
        'may_call_work',
        "home_visit_permission")
    list_display = (
        'subject_visit', 'date_signed', "home_visit_permission",
        "may_follow_up", "may_sms_follow_up", "has_alt_contact",
        "may_call_work", "may_contact_someone")

    def get_actions(self, request):
        actions = super(SubjectLocatorAdmin, self).get_actions(request)
        actions['export_locator_for_cdc_action'] = (
            export_locator_for_cdc_action(
                delimiter='|',
                encrypt=False,
                strip=True,
                exclude=['exported', 'registered_subject',
                         self.visit_attr, 'revision', 'hostname_created',
                         'hostname_modified', 'created', 'modified', 'user_created', 'user_modified', ],
                extra_fields=OrderedDict(
                    {'subject_identifier': self.visit_attr + '__appointment__registered_subject__subject_identifier',
                     'first_name': self.visit_attr + '__appointment__registered_subject__first_name',
                     'last_name': self.visit_attr + '__appointment__registered_subject__last_name',
                     'initials': self.visit_attr + '__appointment__registered_subject__initials',
                     'dob': self.visit_attr + '__appointment__registered_subject__dob',
                     'identity': self.visit_attr + '__appointment__registered_subject__identity',
                     'identity_type': self.visit_attr + '__appointment__registered_subject__identity_type',
                     'plot_identifier': self.visit_attr + '__household_member__household_structure__household_'
                     '_plot__plot_identifier',
                     })
            ),
            'export_locator_for_cdc_action',
            "Export Locator in CDC format (Manual)")
        return actions
