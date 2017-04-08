#!/bin/bash
source /Users/django/.venvs/bcpp/bin/activate && \
cd /Users/django/source/bcpp && \
gunicorn -c gunicorn.conf.py bcpp.wsgi --pid /Users/django/log/gunicorn.pid --daemon
