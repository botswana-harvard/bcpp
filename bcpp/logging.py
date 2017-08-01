import os

from edc_base.logging import verbose_formatter, file_handler
from edc_sync.loggers import loggers as edc_sync_loggers
from edc_sync_files.loggers import loggers as edc_sync_files_loggers


file_handler['filename'] = os.path.join(os.path.expanduser('~/'), 'bcpp.log')

loggers = {}
loggers.update(**edc_sync_loggers)
loggers.update(**edc_sync_files_loggers)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': verbose_formatter,
    },
    'handlers': {
        'file': file_handler
    },
    'loggers': loggers,
}
