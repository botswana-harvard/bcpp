from django.apps import apps as django_apps
from django.contrib.admin.filters import SimpleListFilter

from edc_constants.constants import YES, NO

from .models import HicEnrollment


class HicEnrolledFilter(SimpleListFilter):

    title = _('Hic Enrolled')
    parameter_name = 'hic_enrolled'

    def lookups(self, request, model_admin):
        return ((YES, 'Yes'), (NO, 'No'), )

    def queryset(self, request, queryset):
        Household = django_apps.get_model('bcpp_household', 'Household')
        not_enrolled = []
        enrolled = []
        if isinstance(queryset.all()[0], Household):
            for hs in queryset.all():
                if not HicEnrollment.objects.filter(
                        hic_permission=YES,
                        subject_visit__household_member__household_structure__household=hs).exists():
                    enrolled.append(hs)
                else:
                    not_enrolled.append(hs)
            if self.value() == YES:
                return queryset.filter(household_identifier__in=enrolled)
            if self.value() == NO:
                return queryset.filter(household_identifier__in=not_enrolled)
        else:
            for hs in queryset.all():
                if not HicEnrollment.objects.filter(
                        hic_permission=YES,
                        subject_visit__household_member__household_structure__household__plot=hs).exists():
                    enrolled.append(hs)
                else:
                    not_enrolled.append(hs)
            if self.value() == YES:
                return queryset.filter(plot_identifier__in=enrolled)
            if self.value() == NO:
                return queryset.filter(plot_identifier__in=not_enrolled)
