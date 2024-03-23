#!/bin/bash
python manage.py migrate --settings=memorymap_toolkit.settings.production
python manage.py collectstatic --settings=memorymap_toolkit.settings.production --noinput
python manage.py shell < mmt_setup.py --settings=memorymap_toolkit.settings.production 
gunicorn --bind 0.0.0.0:8000 memorymap_toolkit.wsgi