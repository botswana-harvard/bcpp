from django.urls.base import reverse
from django.views.generic import FormView, TemplateView

from edc_base.view_mixins import EdcBaseViewMixin


class EnumerationDashboardView(EdcBaseViewMixin, TemplateView, FormView):
    template_name = 'bcpp_dashboard/enumeration_dashboard.html'
    project_name = 'BCPP'

    def __init__(self, **kwargs):
        super(EnumerationDashboardView, self).__init__(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            context = self.get_context_data()
            context.update(
                form=form)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('enumeration_dashboard')

    def get_context_data(self, **kwargs):
        context = super(EnumerationDashboardView, self).get_context_data(**kwargs)
        return context
