import arrow

from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, FormView

from edc_base.view_mixins import EdcBaseViewMixin

from plot.models import Plot, PlotLog, PlotLogEntry

from ..forms import SearchPlotForm


class PlotsView(EdcBaseViewMixin, TemplateView, FormView):
    form_class = SearchPlotForm
    template_name = 'plots.html'
    paginate_by = 10
    search_url_name = 'plots_url'
    search_model = Plot

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def search_options(self, search_term):
        return (
            Q(plot_identifier__icontains=search_term) |
            Q(user_created__iexact=search_term) |
            Q(user_modified__iexact=search_term))

    def queryset(self, *options):
        try:
            qs = [self.search_model.objects.get(options)]
        except self.search_model.DoesNotExist:
            qs = None
        except MultipleObjectsReturned:
            qs = self.search_model.objects.filter(options).order_by('-created')
        return qs

    def form_valid(self, form):
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            options = self.search_options(search_term)
            qs = self.queryset(**options)
            if not qs:
                form.add_error('search_term', 'No matching records for \'{}\'.'.format(search_term))
            context = self.get_context_data()
            context.update(form=form, results=self.paginate(qs))
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print('hello')
        plot_results = Plot.objects.all().order_by('-created')
        results = []
        for plot in self.paginate(plot_results):
            try:
                required_plot_models = []
                required_plot_models.append(plot)
                plot_log = PlotLog.objects.get(plot=plot)
                required_plot_models.append(plot_log)
                plot_log_entry = PlotLogEntry.objects.get(
                    plot_log__plot=plot,
                    report_datetime__year=arrow.utcnow().year,
                    report_datetime__month=arrow.utcnow().month,
                    report_datetime__day=arrow.utcnow().day)
                required_plot_models.append(plot_log_entry)
            except PlotLog.DoesNotExist:
                required_plot_models.append(PlotLog.objects.none())
                required_plot_models.append(PlotLogEntry.objects.none())
            except PlotLogEntry.DoesNotExist:
                required_plot_models.append(PlotLogEntry.objects.none())
            except PlotLogEntry.MultipleObjectsReturned:
                required_plot_models.append(PlotLogEntry.objects.filter(plot_log__plot=plot).latest())
            plot_log_entry_link_html_class = "disabled" if plot.confirmed else "active"
            required_plot_models.append(plot_log_entry_link_html_class)
            results.append(required_plot_models)
        context.update(
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
