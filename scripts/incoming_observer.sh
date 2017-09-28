#!/bin/bash

echo "Starting Incoming Observer"

cd ~/source/bcpp && source ~/.venvs/bcpp/bin/activate && \
python manage.py incoming_observer && \
echo "Started Incoming observer."