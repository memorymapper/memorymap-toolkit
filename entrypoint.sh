#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input --settings=memorymap_toolkit.settings.local
python manage.py migrate --settings=memorymap_toolkit.settings.local

exec "$@"
