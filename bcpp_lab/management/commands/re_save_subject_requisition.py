from django.core.management.base import BaseCommand, CommandError

from bhp066.apps.bcpp_lab.models import SubjectRequisition


class Command(BaseCommand):

    APP_NAME = 0
    MODEL_NAME = 1
    args = '<community name e.g otse>'
    help = 'Re save household log entries.'

    def handle(self, *args, **options):
        if not args or len(args) < 1:
            raise CommandError('Missing \'using\' parameters.')
        community_name = args[0]
        subject_requisitions = SubjectRequisition.objects.filter(
            subject_visit__household_member__household_structure__household__plot__community=community_name)
        total_subject_requisitions = len(subject_requisitions)
        count = 0
        for subject_requisition in subject_requisitions:
                subject_requisition.save()
                count += 1
                print count, " of ", total_subject_requisitions
