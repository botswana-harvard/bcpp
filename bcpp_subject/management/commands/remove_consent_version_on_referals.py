from __future__ import print_function
import os
import csv

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    args = 'file path e.g /Users/django/sent_archive/, new_file_path'
    help = 'Remove consent_version referrals, then export the files back to a csv.'

    def handle(self, *args, **options):
        if not args or len(args) < 2:
            raise CommandError('Usage: <command> <source path> <destination path>')
        path = os.path.expanduser(args[0])
        new_path = os.path.expanduser(args[1])
        file_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith(".csv")]
        for file_name in file_list:
            file_path = os.path.join(path, file_name)
            new_file_path = os.path.join(new_path, file_name)
            with open(file_path, 'r') as ref_file, open(new_file_path, "wb") as new_file:
                reader = csv.reader(ref_file, delimiter="|")
                writer = csv.writer(new_file, delimiter="|")
                header = reader.next()
                consent_version = header.index("consent_version")
                header.pop(consent_version)
                writer.writerow(header)
                for row in reader:
                    row.pop(consent_version)
                    writer.writerow(row)
                print(file_name)
