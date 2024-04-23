#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z $DJANGO_DB_HOST 5432; do
    sleep 0.1
done

echo "PostgreSQL started"

python manage.py migrate --settings=memorymap_toolkit.settings.production
python manage.py collectstatic --settings=memorymap_toolkit.settings.production --noinput
python manage.py shell < mmt_setup.py --settings=memorymap_toolkit.settings.production 
gunicorn --bind 0.0.0.0:8000 memorymap_toolkit.wsgi