from django import forms
from django.urls.base import reverse

from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout


class SearchForm(forms.Form):

    search_term = forms.CharField(
        label='Search',
        max_length=36)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper = FormHelper()
        self.helper.form_action = reverse('home_url')
        self.helper.form_id = 'form-search'
        self.helper.form_method = 'post'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            FieldWithButtons('search_term', StrictButton('Search', type='submit')))
        
        
class SearchHouseholdForm(forms.SearchForm):

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse('household_search_url')


class SearchPlotForm(SearchForm):

    def __init__(self, *args, **kwargs):
        super(SearchPlotForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse('plot_search_url')

