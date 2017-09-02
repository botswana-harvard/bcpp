#!/bin/bash
source /Users/django/.venvs/bcpp/bin/activate && \
cd /Users/django/source/bcpp && \
python manage.py export_transactions --send_only=True --target_path=/home/django/media/transactions/incoming
