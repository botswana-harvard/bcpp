import csv
from datetime import datetime
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    args = ''
    help = 'Export subject requisitions.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        from ...models import SubjectRequisition
        date_suffix = datetime.today().strftime('%Y%m%d')
        with open('/tmp/subjectrequisition{0}.csv'.format(date_suffix), 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['requisition_identifier', 'subject_identifier', 'initials', 'dob', 'requisition_datetime',
                             'is_drawn', 'drawn_datetime', 'aliquot_type', 'panel', 'community', 'is_received',
                             'is_received_datetime', 'is_labelled', 'is_labelled_datetime', 'is_packed'])
            for subject_requisition in SubjectRequisition.objects.all():
                writer.writerow([subject_requisition.requisition_identifier,
                                 subject_requisition.subject_visit.appointment.registered_subject.subject_identifier,
                                 subject_requisition.subject_visit.appointment.registered_subject.initials,
                                 subject_requisition.subject_visit.appointment.registered_subject.dob,
                                 subject_requisition.requisition_datetime,
                                 subject_requisition.is_drawn,
                                 subject_requisition.drawn_datetime,
                                 subject_requisition.aliquot_type,
                                 subject_requisition.panel,
                                 subject_requisition.community,
                                 subject_requisition.is_receive,
                                 subject_requisition.is_receive_datetime,
                                 subject_requisition.is_labelled,
                                 subject_requisition.is_labelled_datetime,
                                 subject_requisition.is_packed,
                                 # TODO: hiv_status / referral code
                                 # TODO: hiv_status
                                 # TODO: art_status
                                 ])
        print '/tmp/subjectrequisition{0}.csv'.format(date_suffix)
