from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from edc_constants.choices import YES_NO


class MayContactFilter(SimpleListFilter):

    title = _('may_contact')

    parameter_name = 'may_contact'

    def lookups(self, request, model_admin):
        return YES_NO

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(hic_permission=self.value())
