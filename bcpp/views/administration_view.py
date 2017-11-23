
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import AppConfigViewMixin
from edc_navbar import NavbarViewMixin


class AdministrationView(EdcBaseViewMixin, AppConfigViewMixin, TemplateView):

    app_config_name = 'bcpp'
    template_name = 'bcpp/administration.html'

    navbar_name = 'default'
    navbar_selected_item = 'administration'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(navbar_item_selected='administration')
        return context
