from django.urls.base import reverse
from django.views.generic import FormView, TemplateView

from edc_base.view_mixins import EdcBaseViewMixin

from bcpp.forms import SearchHouseholdForm


class SearchHouseholdView(TemplateView, FormView):
    template_name = 'bcpp_dashboard/search/search_household.html'
    project_name = 'BCPP'
    form_class = SearchHouseholdForm
    paginate_by = 4

    def __init__(self, **kwargs):
        super(SearchHouseholdView, self).__init__(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            context = self.get_context_data()
            context.update(
                form=form)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('household_search_url')

    def get_context_data(self, **kwargs):
        context = super(SearchHouseholdView, self).get_context_data(**kwargs)
        return context
