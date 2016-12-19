from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count


class SubjectCommunityListFilter(SimpleListFilter):

    title = _('community')

    parameter_name = 'community'

    def lookups(self, request, model_admin):
        communities = []
        querystr = 'subject_visit__household_member__household_structure__household__plot__map_area'
        for item in [item['subject_visit__household_member__household_structure__household__plot__map_area']
                     for item in model_admin.model.objects.values(querystr).annotate(Count(querystr))]:
            communities.append((item, item))
        return tuple(communities)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                subject_visit__household_member__household_structure__household__plot__map_area=self.value())
