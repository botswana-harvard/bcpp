from django.urls.base import reverse
from django.views.generic import FormView, TemplateView

from bcpp.forms import SearchBHSSubjectForm


class BHSSubjectSearchView(TemplateView, FormView):
    template_name = 'bcpp_dashboard/bhs_subjects.html'
    project_name = 'BCPP'
    form_class = SearchBHSSubjectForm
    paginate_by = 4

    def get_success_url(self):
        return reverse('bhs_subject_search')

    def get_context_data(self, **kwargs):
        context = super(BHSSubjectSearchView, self).get_context_data(**kwargs)
        return context
