#!/bin/bash

cd ~/source/bcpp && source ~/.venvs/bcpp/bin/activate && \
python manage.py deserialize_observer --src_path=/home/django/media/transactions/pending/community_name/
