from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _


class SubjectReferralIsReferredListFilter(SimpleListFilter):

    title = _('referred')

    parameter_name = 'referred'

    def lookups(self, request, model_admin):
        return ((True, 'Yes'), (False, 'No'), )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.exclude(referral_code__in=['NOT-REF', 'ERROR'])
        if not self.value():
            return queryset.filter(referral_code__in=['NOT-REF', 'ERROR'])
