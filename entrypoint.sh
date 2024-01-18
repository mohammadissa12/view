#!/usr/bin/bash

python manage.py migrate --noinput
python manage.py collectstatic --noinput

#DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput
chmod -R 755 /django-app/media
# Or change ownership, replacing 'nginx' with the user that Nginx runs as, if it's different
chown -R nginx:nginx /django-app/media
#create a new superuser
#python manage.py createsuperuser

gunicorn conf.wsgi:application --bind 0.0.0.0:8000

