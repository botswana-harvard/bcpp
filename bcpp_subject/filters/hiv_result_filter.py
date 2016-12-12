from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _


class HivResultFilter(SimpleListFilter):

    title = _('hiv result')

    parameter_name = 'hiv_result'

    def lookups(self, request, model_admin):
        return (('POS', 'HIV Positive'), ('NEG', 'HIV Negative'),
                ('IND', 'Indeterminate'), ('Declined', 'declined'),
                ('Not performed', 'not performed'),)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(hiv_result=self.value())
