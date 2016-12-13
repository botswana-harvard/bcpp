# import copy
# import csv
# import os
#
# from django.core.management.base import BaseCommand, CommandError
#
# from bhp066.apps.member.models import HouseholdMember
# from bhp066.apps.bcpp_subject.models.subject_consent import SubjectConsent
#
#
# class Command(BaseCommand):
#
#     args = 'csv_filename'
#     help = ('Import subject_identifier corrections from the given filename. '
#             'Format is subject_identifier, community, subject_identifier_aka, dm_comment')
#
#     def handle(self, *args, **options):
#         try:
#             import_filename = args[0]
#         except IndexError:
#             raise CommandError('Expected at least one parameter for csv_filename to import')
#         n = 0
#         header_row = []
#         SUBJECT_IDENTIFIER = 0
#         COMMUNITY = 1
#         SUBJECT_IDENTIFIER_AKA = 2
#         DM_COMMENT = 3
#
#         filename = os.path.expanduser('~/subject_identifier_{}.csv')
#         with open(filename.format(import_filename), 'w') as file_object:
#             rows = csv.reader(file_object, delimiter=',')
#             for i, row in enumerate(rows):
#                 if not header_row:
#                     # set the header row list
#                     header_row = [item for item in copy.deepcopy(row)]
#                     if header_row != ['subject_identifier', 'community', 'subject_identifier_aka', 'dm_comment']:
#                         raise CommandError(
#                             'Expected header of {}'.format(', '.join([
#                                 'subject_identifier', 'community', 'subject_identifier_aka', 'dm_comment'])))
#                 else:
#                     # confirm subject_identifier not in edc
#                     RegisteredSubject.objects.get(subject_identifier=row[SUBJECT_IDENTIFIER])
#                     raise
#             for i, row in enumerate(rows):
#                 for hm in HouseholdMember.objects.filter(
#                     household_structure__survey__survey_slug='bcpp-year-1',
#                     registered_subject__subject_identifier__startswith='066'
#                     ).order_by('registered_subject__subject_identifier'):
#                 n += 1
#                 try:
#                     # hm.registered_subject attributes should equal subject_consent
#                     SubjectConsent.objects.get(
#                         household_member=hm,
#                         subject_identifier=hm.registered_subject.subject_identifier,
#                         subject_identifier_aka=hm.registered_subject.subject_identifier_aka,
#                         )
#                 except SubjectConsent.DoesNotExist:
#                     raise CommandError('Inconsistent identifiers between SubjectConsent and '
#                                        'RegisteredSubject. Got {}.'.format(hm.registered_subject))
#                 writer.writerow(
#                     [hm.registered_subject.subject_identifier,
#                      hm.household_structure.household.plot.community,
#                      hm.registered_subject.subject_identifier_aka,
#                      hm.registered_subject.dm_reference]
#                     )
#         print 'Exported {} identifiers to {}'.format(n, filename)
