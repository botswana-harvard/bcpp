from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _


class Cd4ThreshHoldFilter(SimpleListFilter):

    title = _('cd4 threshhold')

    parameter_name = 'threshold'

    def lookups(self, request, model_admin):
        return (('>350', '>350'), ('<=350', '<=350'))

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == '>350':
                return queryset.filter(cd4_value__gt=350)
            elif self.value() == '<=350':
                return queryset.filter(cd4_value__lte=350)
            else:
                return queryset
