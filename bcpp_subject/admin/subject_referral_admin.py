from collections import OrderedDict

from django.contrib import admin

from edc_export.actions import export_as_csv_action

from ..actions import export_referrals_for_cdc_action
from ..admin_site import bcpp_subject_admin
from ..models import SubjectReferral
from ..forms import SubjectReferralForm
from ..filters import SubjectCommunityListFilter, SubjectReferralIsReferredListFilter

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SubjectReferral, site=bcpp_subject_admin)
class SubjectReferralAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SubjectReferralForm

    date_hierarchy = 'referral_appt_date'

    search_fields = ['subject_visit__appointment__registered_subject__first_name',
                     'subject_visit__appointment__registered_subject__subject_identifier']

    list_display = [
        'subject_visit',
        'report_datetime',
        'dashboard',
        'subject_referred',
        'referral_code',
        'referral_clinic_type',
        'referral_appt_date',
        'exported',
        'exported_datetime',
        'in_clinic_flag',
    ]

    list_filter = ['exported', 'in_clinic_flag',
                   SubjectReferralIsReferredListFilter,
                   SubjectCommunityListFilter,
                   'referral_code', 'report_datetime', 'referral_appt_date', 'exported_datetime', 'hostname_created']

    fields = (
        'subject_visit',
        'report_datetime',
        'subject_referred',
        'scheduled_appt_date',
        'referral_appt_comment',
        'comment'
    )

    radio_fields = {
        "referral_code": admin.VERTICAL,
        "subject_referred": admin.VERTICAL,
        "referral_appt_comment": admin.VERTICAL,
    }

    def get_actions(self, request):
        actions = super(SubjectReferralAdmin, self).get_actions(request)
        actions['export_as_csv_action'] = (  # This is a django SortedDict (function, name, short_description)
            export_as_csv_action(
                delimiter=',',
                encrypt=False,
                strip=True,
                exclude=['exported', 'exported_datetime', self.visit_attr, 'revision',
                         'hostname_created', 'hostname_modified', 'created', 'modified',
                         'user_created', 'user_modified', 'comment'],
                extra_fields=OrderedDict(
                    {'first_name': self.visit_attr + '__appointment__registered_subject__first_name',
                     'last_name': self.visit_attr + '__appointment__registered_subject__last_name',
                     'initials': self.visit_attr + '__appointment__registered_subject__initials',
                     'dob': self.visit_attr + '__appointment__registered_subject__dob',
                     'identity': self.visit_attr + '__appointment__registered_subject__identity',
                     'identity_type': self.visit_attr + '__appointment__registered_subject__identity_type',
                     })
            ),
            'export_as_csv_action',
            'Export Referrals to CSV')
        actions['export_referrals_for_cdc_action'] = (
            export_referrals_for_cdc_action(
                delimiter='|',
                encrypt=False,
                strip=True,
                exclude=[
                    'comment',
                    'created',
                    'exported',
                    'hostname_created',
                    'hostname_modified',
                    'in_clinic_flag',
                    'modified',
                    'referral_clinic_other',
                    'scheduled_appt_date',
                    'revision',
                    'subject_visit',
                    'user_created',
                    'user_modified'],
                extra_fields=OrderedDict(
                    {'plot_identifier': self.visit_attr + '''__household_member__household_structure__household_'''
                     '''_plot__plot_identifier''',
                     'dob': self.visit_attr + '__appointment__registered_subject__dob',
                     'first_name': self.visit_attr + '__appointment__registered_subject__first_name',
                     'identity': self.visit_attr + '__appointment__registered_subject__identity',
                     'identity_type': self.visit_attr + '__appointment__registered_subject__identity_type',
                     'initials': self.visit_attr + '__appointment__registered_subject__initials',
                     'last_name': self.visit_attr + '__appointment__registered_subject__last_name',
                     })
            ),
            'export_referrals_for_cdc_action',
            'Export Referrals in CDC format (Manual)')
        return actions
