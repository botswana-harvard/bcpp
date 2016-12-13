from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from ..models import SubjectReferral, SubjectLocator


class SubjectLocatorIsReferredListFilter(SimpleListFilter):

    title = _('referred')

    parameter_name = 'referred'

    def lookups(self, request, model_admin):
        return ((True, 'Yes'), (False, 'No'), )

    def queryset(self, request, queryset):
        locators = []
        if self.value():
            for obj in queryset:
                refferal = SubjectReferral.objects.filter(
                    subject_visit__appointment__registered_subject__subject_identifier=obj.subject_identifier).exclude(
                        referral_code__in=['NOT-REF', 'ERROR'])
                if refferal:
                    locators.append(obj.subject_identifier)
            queryset = SubjectLocator.objects.filter(subject_identifier__in=locators)
        if not self.value():
            for obj in queryset:
                refferal = SubjectReferral.objects.filter(
                    subject_visit__appointment__registered_subject__subject_identifier=obj.subject_identifier,
                    referral_code__in=['NOT-REF', 'ERROR'])
                if refferal:
                    locators.append(obj.subject_identifier)
            queryset = SubjectLocator.objects.filter(subject_identifier__in=locators)
        return queryset
