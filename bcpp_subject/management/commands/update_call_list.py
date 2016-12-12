from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_model

from bhp066.apps.bcpp.choices import COMMUNITIES
from bhp066.apps.bcpp_survey.models import Survey


class Command(BaseCommand):

    args = 'community source-survey-slug label'
    help = 'Add to the call list info from all subject consents from the specified survey.'

    def handle(self, *args, **options):
        from bhp066.apps.bcpp_subject.classes import UpdateCallList
        CallList = get_model('bcpp_subject', 'CallList')
        count = CallList.objects.all().count()
        try:
            community = args[0]
        except IndexError:
            raise CommandError('Specify a community')
        community_names = [str(cm[1]).lower() for cm in COMMUNITIES]
        if community not in community_names:
            raise CommandError('Please enter a valid community. {} is not valid.'.format(community.upper()))
        try:
            survey_slug = args[1]
            Survey.objects.get(survey_slug=survey_slug)
        except (IndexError, Survey.DoesNotExist):
            raise CommandError('Specify a valid survey_slug')
        try:
            label = args[2]
        except IndexError:
            raise CommandError('Specify a label')
        UpdateCallList().update_call_list(community, survey_slug, label, verbose=True)
        new_count = CallList.objects.all().count()
        print 'Added {} records to the Call List for {}: {}.'.format(new_count - count, survey_slug, label)
