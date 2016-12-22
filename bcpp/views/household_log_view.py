from django.urls.base import reverse
from django.views.generic import FormView, TemplateView

from edc_base.view_mixins import EdcBaseViewMixin


class HouseholdLogView(EdcBaseViewMixin, TemplateView):
    template_name = 'bcpp_composition.html'

    def __init__(self, **kwargs):
        super(HouseholdLogView, self).__init__(**kwargs)

#     def form_valid(self, form):
#         if form.is_valid():
#             context = self.get_context_data()
#             context.update(
#                 form=form)
#         return self.render_to_response(context)

    def get_success_url(self):
        return reverse('household_composition')

    def get_context_data(self, **kwargs):
        context = super(HouseholdLogView, self).get_context_data(**kwargs)
        return context
