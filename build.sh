#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python one_time_superuser.py

python manage.py collectstatic --no-input
python manage.py migrate
