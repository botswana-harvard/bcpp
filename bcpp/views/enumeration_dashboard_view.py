from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin


class EnumerationDashboardView(EdcBaseViewMixin, TemplateView):

    template_name = 'bcpp_dashboard/enumeration_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            site_header=admin.site.site_header,
        )
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EnumerationDashboardView, self).dispatch(*args, **kwargs)
