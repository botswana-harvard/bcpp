import os

bind = "127.0.0.1:9000"  # Don't use port 80 because nginx occupied it already.
errorlog = os.path.expanduser('~/logs/gunicorn-error.log')
accesslog = os.path.expanduser('~/logs/gunicorn-access.log')
loglevel = 'info'
workers = 8  # the number of recommended workers is '2 * number of CPUs + 1'
timeout = 300
