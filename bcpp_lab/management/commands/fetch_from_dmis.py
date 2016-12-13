# from optparse import make_option
#
# from django.core.management.base import BaseCommand, CommandError
#
# # from bhp066.config.celery import already_running, CeleryTaskAlreadyRunning, CeleryNotRunning
#
# # from ...classes import Dmis
#
#
# class Command(BaseCommand):
#     """ thsi has not been tested, yet. But the class Dmis works."""
#     args = ''
#     help = ('fetch receiving and result data from LIS and/or csv file of '
#             'identifiers into a csv file. Either --filename or --protocol_number are required')
#     option_list = BaseCommand.option_list
#     option_list += (
#         make_option('--csv-file',
#             action='store_true',
#             dest='filename',
#             default=False,
#             help=('CSV filename for identifiers to be read in. Defaults to None')),
#         make_option('--csv-columns',
#             action='store_true',
#             dest='csv_columns',
#             default=False,
#             help=('Comma separated list of column numbers (zero-based) '
#                   'to read in identifiers from the CSV file. Defaults to column 0.')),
#         make_option('--dmis-column',
#             action='store_true',
#             dest='dmis_column',
#             default=False,
#             help=('Identifier column name in DMIS. Defaults to \'edc_specimen_identifier\'' )),
#         )
#
#     def handle(self, *args, **options):
#         """See class docstring for usage."""
#         filename = None
#         protocol_number = None
#         if options['filename']:
#             filename = options['filename']
#         if options['csv_columns']:
#             data_column_numbers = options['csv_columns'].split(',')
#         else:
#             data_column_numbers = [0]
#         if options['dmis_column']:
#             dmis_column = options['dmis_column']
#         else:
#             dmis_column = 'edc_specimen_identifier'
#         if options['protocol_number']:
#             protocol_number = options['protocol_number']
#         try:
#             dmis = Dmis(filename,
#                         data_column_numbers=data_column_numbers,
#                         dmis_column=dmis_column,
#                         protocol_number=protocol_number,
#                         verbose=True)
#             already_running(dmis.load_and_dump)
#             result = dmis.load_and_dump.delay(print_messages=True)
#             print(('Task has been sent to the queue. Result: {0.result!r} ID: {0.id})'
#                    ).format(result))
#         except CeleryTaskAlreadyRunning as already_running:
#             raise CommandError(str(already_running))
#         except CeleryNotRunning as not_running:
#             raise CommandError(str(not_running))
#         except Exception as e:
#             raise CommandError('Unable to run task. Celery got {}.'.format(str(e)))
