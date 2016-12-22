from django.db.models import Q
from django.views.generic import FormView, TemplateView

from edc_base.view_mixins import EdcBaseViewMixin

from bcpp.forms import SearchHouseholdForm
from household.models.household import Household
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import MultipleObjectsReturned


class QuerysetWrapper:
    def __init__(self, qs):
        self.qs = qs or []
        self._object_list = []

    @property
    def object_list(self):
        if not self._object_list:
            for obj in self.qs:
                try:
                    household = Household.objects.get(household_identifier=obj.household_identifier)
                    obj.household_identifier = household.household_identifier
                except Household.MultipleObjectsReturned:
                    households = Household.objects.filter(plot_identifier=obj.plot_identifier)
                    obj.household_identifier = households[0].household_identifier
                except Household.DoesNotExist:
                    obj.household_identifier = None
                self._object_list.append(obj)
        return self._object_list


class SearchHouseholdView(EdcBaseViewMixin, TemplateView, FormView):
    template_name = 'search/search_household.html'
    subject_dashboard_url_name = 'household_search'
    search_url_name = 'household_search'
    form_class = SearchHouseholdForm
    paginate_by = 4

    def __init__(self, **kwargs):
        super(SearchHouseholdView, self).__init__(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            options = (
                Q(plot_identifier__icontains=search_term) |
                Q(user_created__iexact=search_term) |
                Q(user_modified__iexact=search_term)
            )
            try:
                qs = [Household.objects.get(options)]
            except Household.DoesNotExist:
                qs = None
                form.add_error(
                    'search_term',
                    'No matching records for \'{}\'.'.format(search_term))
            except MultipleObjectsReturned:
                qs = Household.objects.filter(options).order_by('household_identifier', '-created')
            context = self.get_context_data()
            context.update(
                form=form,
                results=self.paginate(QuerysetWrapper(qs).object_list))
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(SearchHouseholdView, self).get_context_data(**kwargs)
        qs = Household.objects.all().order_by('household_identifier', '-created')
        results = QuerysetWrapper(qs).object_list
        context.update(
            # site_header=admin.site.site_header,
            subject_dashboard_url_name=self.subject_dashboard_url_name,
            search_url_name=self.search_url_name,
            results=self.paginate(results))
        return context

    def paginate(self, qs):
        paginator = Paginator(qs, self.paginate_by)
        try:
            page = paginator.page(self.kwargs.get('page', 1))
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return page
