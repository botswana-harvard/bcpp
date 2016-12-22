from django.urls.base import reverse
from django.views.generic import FormView, TemplateView

from edc_base.view_mixins import EdcBaseViewMixin

from bcpp.forms import SearchSubjectForm


class SearchSubjectView(EdcBaseViewMixin, TemplateView, FormView):
    template_name = 'search/search_subjects.html'
    form_class = SearchSubjectForm
    paginate_by = 4

    def __init__(self, **kwargs):
        super(SearchSubjectView, self).__init__(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            context = self.get_context_data()
            context.update(
                form=form)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('subject_search')

    def get_context_data(self, **kwargs):
        context = super(SearchSubjectView, self).get_context_data(**kwargs)
        return context
