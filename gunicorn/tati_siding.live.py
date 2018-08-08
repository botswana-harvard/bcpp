# uat.ambition gunicorn.conf
import os

from pathlib import Path

SOURCE_ROOT = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

errorlog = os.path.join(
    SOURCE_ROOT, 'log/bcpp-live-tati_siding-gunicorn-error.log')
accesslog = os.path.join(
    SOURCE_ROOT, 'log/bcpp-live-tati_siding-gunicorn-access.log')
loglevel = 'debug'
pidfile = os.path.join(SOURCE_ROOT, 'run/bcpp-live-tati_siding.pid')

workers = 2  # the number of recommended workers is '2 * number of CPUs + 1'

raw_env = ['DJANGO_SETTINGS_MODULE=bcpp.community.tati_siding']

bind = "127.0.0.1:9038"