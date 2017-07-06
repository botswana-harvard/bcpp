from datetime import date, datetime, time

from django.core.management.base import BaseCommand
from django.conf import settings
from bcpp.exim.export_data.export_confirmation_file import ExportConfirmationFile


class Command(BaseCommand):
    help = 'Export sync confirmation file.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--daily_report',
            action='store_true',
            dest='daily_report',
            default=False,
            help='Generates sync confirmation report.',
        )

    def handle(self, *args, **options):
            export = ExportConfirmationFile(
                verbose=True,
                community=settings.CURRENT_MAP_AREA,
                start_date=datetime.combine(date.today(), time.min),
                end_date=datetime.combine(date.today(), time.max))
            export.create_subject_consents_file()
            export.create_subjectvisits_file()
            export.crfs_file()
