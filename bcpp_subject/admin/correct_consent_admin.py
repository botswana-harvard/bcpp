from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..forms import CorrectConsentForm
from ..models import CorrectConsent, SubjectConsent


@admin.register(CorrectConsent, site=bcpp_subject_admin)
class CorrectConsentAdmin(admin.ModelAdmin):

    form = CorrectConsentForm

    fields = (
        'subject_consent',
        'report_datetime',
        'old_last_name',
        'new_last_name',
        'old_first_name',
        'new_first_name',
        'old_initials',
        'new_initials',
        'old_dob',
        'new_dob',
        'old_gender',
        'new_gender',
        'old_guardian_name',
        'new_guardian_name',
        'old_may_store_samples',
        'new_may_store_samples',
        'old_is_literate',
        'new_is_literate',
        'new_witness_name',
        'old_witness_name',
    )

    list_display = ('subject_consent', 'report_datetime')

    list_filter = ('report_datetime', 'created', 'modified')

    search_fields = (
        'subject_consent__subject_identifier', 'new_first_name', 'old_first_name', 'new_last_name', 'old_last_name')

    radio_fields = {
        'old_gender': admin.VERTICAL,
        'new_gender': admin.VERTICAL,
        'old_is_literate': admin.VERTICAL,
        'new_is_literate': admin.VERTICAL,
        'old_may_store_samples': admin.VERTICAL,
        'new_may_store_samples': admin.VERTICAL,
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject_consent":
            kwargs["queryset"] = SubjectConsent.objects.filter(id__exact=request.GET.get('subject_consent', 0))
        return super(CorrectConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
