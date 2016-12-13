from django import forms

from ..models import CommunityEngagement

from .form_mixins import SubjectModelFormMixin


class CommunityEngagementForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(CommunityEngagementForm, self).clean()
        the_problems_list = []
        for problems in cleaned_data.get('problems_engagement'):
            the_problems_list.append(problems.name)
        if 'Don\'t want to answer' in the_problems_list and len(cleaned_data.get('problems_engagement')) > 1:
            raise forms.ValidationError(
                'You cannot choose Don\'t want to answer and another problem at the same time. Please correct')

        return cleaned_data

    class Meta:
        model = CommunityEngagement
        fields = '__all__'
