import csv
from datetime import datetime
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    args = ''
    help = 'Export aliquots.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        from ...models import Aliquot
        date_suffix = datetime.today().strftime('%Y%m%d')
        with open('/tmp/aliquot{0}.csv'.format(date_suffix), 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['requisition_identifier', 'drawn_datetime', 'aliquot_identifier',
                             'aliquot_type', 'aliquot_datetime', 'subject_identifier', 'initials',
                             'dob', 'requisition_model_name', 'receive_identifier'])
            for a in Aliquot.objects.all():
                writer.writerow([a.receive.requisition_identifier,
                                 a.receive.drawn_datetime,
                                 a.aliquot_identifier,
                                 a.aliquot_type, a.aliquot_datetime,
                                 a.receive.registered_subject.subject_identifier,
                                 a.receive.registered_subject.initials,
                                 a.receive.registered_subject.dob,
                                 a.receive.requisition_model_name,
                                 # TODO: hiv_status / referral code
                                 # TODO: hiv_status
                                 # TODO: art_status
                                 a.receive.receive_identifier])
