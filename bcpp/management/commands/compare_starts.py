import csv

from django.apps import apps as django_apps
from django.core.management.base import BaseCommand

from bcpp_subject.models import SubjectConsent, SubjectRequisition
from member.models import HouseholdMember


def year_3_consents(using=None):
    using = using or 'default'
    return SubjectConsent.objects.filter(
        survey_schedule__icontains='bcpp-survey.bcpp-year-3', using=using)


def year_3_members(using=None):
    using = using or 'default'
    return HouseholdMember.objects.filter(
        survey_schedule__icontains='bcpp-survey.bcpp-year-3', using=using)


def year_3_requisitions(using=None):
    using = using or 'default'
    return SubjectRequisition.objects.filter(
        subject_visit__survey_schedule__icontains='bcpp-survey.bcpp-year-3',
        using=using)


class Command(BaseCommand):

    help = 'Create a statistics file for server vs client.'

    def add_arguments(self, parser):
        parser.add_argument('remote_host', type=str, help='remote_host e.g bcpp026')

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.NOTICE('Preparing to the report ...'))
        remote_host = options['remote_host']
        report_dict = {}
        #  Compare consents.
        if year_3_consents(remote_host) and year_3_consents().count():
            if year_3_consents(remote_host).count() != year_3_consents().count():
                report_dict.update(
                    server_consents=year_3_consents().count(),
                    client_consents=year_3_consents(remote_host).count())
        else:
            self.stdout.write(
                self.style.NOTICE('Something may be wrong both '
                                  'machines should have some data ...'))

        #  Compare members.
        if year_3_members(remote_host).count() and year_3_members().count():
            if year_3_members(remote_host).count() != year_3_members().count():
                report_dict.update(
                    server_members=year_3_members().count(),
                    client_members=year_3_members(remote_host).count())
        else:
            self.stdout.write(
                self.style.NOTICE('Something may be wrong both '
                                  'machines should have some data ...'))

        #  Compare subject requisitions.
        if year_3_requisitions(remote_host).count() and year_3_requisitions().count():
            if year_3_requisitions(remote_host).count() != year_3_requisitions().count():
                report_dict.update(
                    server_members=year_3_requisitions().count(),
                    client_members=year_3_requisitions(remote_host).count())
        else:
            self.stdout.write(
                self.style.NOTICE('Something may be wrong both '
                                  'machines should have some data ...'))
        report_name = remote_host + '.csv'
        if report_dict:
            with open(report_name, 'wb') as csv_file:
                writer = csv.writer(csv_file)
                for key, value in report_dict.items():
                    writer.writerow([key, value])
        self.stdout.write(self.style.NOTICE(f'file {report_name} generated.'))
