from django import forms

from ..models import ViralLoadResult


class ViralLoadResultForm (forms.ModelForm):

    class Meta:
        model = ViralLoadResult
        fields = '__all__'
