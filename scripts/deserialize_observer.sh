#!/bin/bash

echo "Starting deserialize observer"

cd ~/source/bcpp && source ~/.venvs/bcpp/bin/activate && \
python manage.py deserialize_observer && \
echo "Started deserialize observer."