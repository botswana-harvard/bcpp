from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import AppConfigViewMixin


class HomeView(EdcBaseViewMixin, AppConfigViewMixin, TemplateView):

    app_config_name = 'bcpp'
    template_name = 'bcpp/home.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            navbar_item_selected='home',
            map_area=settings.CURRENT_MAP_AREA,
            ANONYMOUS_ENABLED=settings.ANONYMOUS_ENABLED)
        return context
