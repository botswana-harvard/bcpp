from django.contrib import admin

from edc_base.modeladmin_mixins import TabularInlineMixin

from ..admin_site import bcpp_subject_admin
from ..forms import GrantForm
from ..models import LabourMarketWages, Grant

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Grant, site=bcpp_subject_admin)
class GrantAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = GrantForm
    fields = ('labour_market_wages', 'grant_number', 'grant_type', 'other_grant',)
    list_display = ('labour_market_wages', 'grant_number', 'grant_type', 'other_grant', )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "labour_market_wages":
            kwargs["queryset"] = LabourMarketWages.objects.filter(id__exact=request.GET.get('labour_market_wages', 0))
        return super(GrantAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class GrantInlineAdmin(TabularInlineMixin, admin.TabularInline):
    model = Grant
    form = GrantForm
    extra = 1
    fields = ('grant_number', 'grant_type', 'other_grant',)
    list_display = ('grant_number', 'grant_type', 'other_grant', )
