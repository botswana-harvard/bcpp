# uat.ambition gunicorn.conf
import os

from pathlib import Path

SOURCE_ROOT = str(Path(os.path.dirname(os.path.abspath(__file__))).parent)

errorlog = os.path.join(
    SOURCE_ROOT, 'log/bcpp-live-masunga-gunicorn-error.log')
accesslog = os.path.join(
    SOURCE_ROOT, 'log/bcpp-live-masunga-gunicorn-access.log')
loglevel = 'debug'
pidfile = os.path.join(SOURCE_ROOT, 'run/bcpp-live-masunga.pid')

workers = 2  # the number of recommended workers is '2 * number of CPUs + 1'

raw_env = ['DJANGO_SETTINGS_MODULE=bcpp.community.masunga']

bind = "127.0.0.1:9018"