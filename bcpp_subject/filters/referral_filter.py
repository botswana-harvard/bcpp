from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from ..choices import REFERRAL_CODES


class MayContactFilter(SimpleListFilter):

    title = _('may_contact')

    parameter_name = 'may_contact'

    def lookups(self, request, model_admin):
        return REFERRAL_CODES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(referral_code=self.value())
