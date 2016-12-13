from django.apps import apps as django_apps
from django.contrib import admin

from edc_consent.modeladmin_mixins import ModelAdminConsentMixin

from ..admin_site import bcpp_subject_admin
from ..forms import SubjectConsentForm
from ..models import SubjectConsent


@admin.register(SubjectConsent, site=bcpp_subject_admin)
class SubjectConsentAdmin(ModelAdminConsentMixin, admin.ModelAdmin):

    form = SubjectConsentForm

    search_fields = ('household_member__household_structure__household__plot__plot_identifier',
                     'household_member__household_structure__household__household_identifier')
    radio_fields = {"is_minor": admin.VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            HouseholdMember = django_apps.get_model('member', 'householdmember')
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member', 0))
        return super(SubjectConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
