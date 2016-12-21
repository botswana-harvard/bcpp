from django.urls.base import reverse
from django.views.generic import FormView, TemplateView

from bcpp.forms import SearchHouseholdForm


class SearchHouseholdView(TemplateView, FormView):
    template_name = 'bcpp_dashboard/search_household.html'
    project_name = 'BCPP'
    form_class = SearchHouseholdForm
    paginate_by = 4

    def get_success_url(self):
        return reverse('household_search_url')

    def get_context_data(self, **kwargs):
        context = super(SearchHouseholdView, self).get_context_data(**kwargs)
        return context
