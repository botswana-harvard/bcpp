#!/bin/bash

cd /home/django/source/bcpp && source /home/django/.venvs/bcpp/bin/activate && \
python manage.py incoming_observer --src_path=/home/django/media/transactions/incoming/community_name/ --dst_path=/home/django/media/transactions/pending/community_name/