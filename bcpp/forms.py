import pytz

from datetime import datetime, time

from django import forms
from django.db.models import Q
from django.urls.base import reverse

from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout


class BHSSearchForm(forms.Form):

    search_term = forms.CharField(
        label='Search',
        max_length=36)

    def __init__(self, *args, **kwargs):
        super(BHSSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper = FormHelper()
        self.helper.form_action = reverse('home_url')
        self.helper.form_id = 'form-patient-search'
        self.helper.form_method = 'post'
        self.helper.html5_required = True
        self.helper.layout = Layout(
            FieldWithButtons('search_term', StrictButton('Search', type='submit')))
