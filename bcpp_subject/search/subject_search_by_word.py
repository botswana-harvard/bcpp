from django.db.models import Q

from edc.dashboard.search.classes import BaseSearchByWord

from ..models import SubjectConsent


class SubjectSearchByWord(BaseSearchByWord):

    name = 'word'
    order_by = ['-created']
    search_model = SubjectConsent
    template = 'subjectconsent_include.html'

    @property
    def qset(self):
        qset = self.qset_for_consent
        qset.add(Q(
            household_member__household_structure__household__household_identifier__icontains=self.search_value), Q.OR)
        qset.add(Q(
            household_member__household_structure__household__plot__plot_identifier__icontains=self.search_value), Q.OR)
        return qset
