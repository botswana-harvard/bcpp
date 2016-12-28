from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from edc_base.view_mixins import EdcBaseViewMixin

from plot.models import Plot, PlotLog, PlotLogEntry

from ..forms import SearchPlotForm


class QuerysetWrapper:
    def __init__(self, qs):
        self.qs = qs or []
        self._object_list = []

    @property
    def object_list(self):
        if not self._object_list:
            for obj in self.qs:
                try:
                    plot = Plot.objects.get(plot_identifier=obj.plot_identifier)
                    obj.plot_identifier = plot.plot_identifier
                except MultipleObjectsReturned:
                    plots = Plot.objects.filter(plot_identifier=obj.plot_identifier)
                    obj.plot_identifier = plots[0].plot_identifier
                except Plot.DoesNotExist:
                    obj.plot_identifier = None
                self._object_list.append(obj)
        return self._object_list


class SearchPlotView(EdcBaseViewMixin, TemplateView, FormView):
    form_class = SearchPlotForm
    template_name = 'search/search_plot.html'
    paginate_by = 10
    subject_dashboard_url_name = 'plot_search_url'
    search_url_name = 'plot_search_url'

    def __init__(self, **kwargs):
        self.maternal_eligibility = None
        super(SearchPlotView, self).__init__(**kwargs)

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(S:aqqearchPlotView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            options = (
                Q(plot_identifier__icontains=search_term) |
                Q(user_created__iexact=search_term) |
                Q(user_modified__iexact=search_term)
            )
            try:
                qs = [Plot.objects.get(options)]
            except Plot.DoesNotExist:
                qs = None
                form.add_error(
                    'search_term',
                    'No matching records for \'{}\'.'.format(search_term))
            except MultipleObjectsReturned:
                qs = Plot.objects.filter(options).order_by('-created')
            context = self.get_context_data()
            context.update(
                form=form,
                results=self.paginate(QuerysetWrapper(qs).object_list))
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(SearchPlotView, self).get_context_data(**kwargs)
        qs = Plot.objects.all().order_by('-created')
        paginated_results = QuerysetWrapper(qs).object_list
        results_log = []
        for plot in self.paginate(paginated_results):
            try:
                required_plot_models = []
                required_plot_models.append(plot)
                plot_log = PlotLog.objects.get(plot=plot)
                required_plot_models.append(plot_log)
                plot_entry = PlotLogEntry.objects.get(plot_log__plot=plot)
                required_plot_models.append(plot_entry)
            except PlotLog.DoesNotExist:
                required_plot_models.append(PlotLog.objects.none())
                required_plot_models.append(PlotLogEntry.objects.none())
            except PlotLogEntry.DoesNotExist:
                required_plot_models.append(PlotLogEntry.objects.none())
            except PlotLogEntry.MultipleObjectsReturned:
                required_plot_models.append(PlotLogEntry.objects.filter(plot_log__plot=plot).latest())
            results_log.append(required_plot_models)
        context.update(
            # site_header=admin.site.site_header,
            subject_dashboard_url_name=self.subject_dashboard_url_name,
            search_url_name=self.search_url_name,
            results=self.paginate(results_log))
        return context

    def paginate(self, qs):
        paginator = Paginator(qs, self.paginate_by)
        try:
            page = paginator.page(self.kwargs.get('page', 1))
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return page
