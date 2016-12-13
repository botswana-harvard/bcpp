# from django.core.management.base import BaseCommand, CommandError
#
# from bhp066.config.celery import already_running, CeleryTaskAlreadyRunning, CeleryNotRunning
#
# from ...tasks import reconcile_packing_list
#
#
# class Command(BaseCommand):
#
#     args = ''
#     help = 'Update packing list from mssql LIS.'
#     option_list = BaseCommand.option_list
#
#     def handle(self, *args, **options):
#         """Flags packing list items as received based on queries into LIS database at
#         settings.LAB_IMPORT_DMIS_DATA_SOURCE.
#
#         Queries BHHRL LIS receiving records and storage records."""
#
#         try:
#             already_running(reconcile_packing_list)
#             result = reconcile_packing_list.delay(print_messages=True)
#             print(('Task has been sent to the queue. Result: {0.result!r} ID: {0.id})'
#                    ).format(result))
#         except CeleryTaskAlreadyRunning as already_running:
#             raise CommandError(str(already_running))
#         except CeleryNotRunning as not_running:
#             raise CommandError(str(not_running))
#         except Exception as e:
#             raise CommandError('Unable to run task. Celery got {}.'.format(str(e)))
