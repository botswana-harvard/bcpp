#!/bin/bash
source /Users/django/.venv/bcpp/bin/activate && \
cd /Users/django/source/bcpp && \
gunicorn -c gunicorn.conf.py bcpp.wsgi --pid /Users/django/logs/gunicorn.pid --daemon