#!/bin/bash

if [ ! -f manage.py ]
then
  django-admin startproject app .
fi

sleep 3

python manage.py makemigrations
python manage.py migrate --noinput

if [[ ! -z "${DJANGO_SU_NAME}" ]]
then
  echo "from django.contrib.auth.models import User; User.objects.filter(username='${DJANGO_SU_NAME}').exists() or User.objects.create_superuser('${DJANGO_SU_NAME}', '${DJANGO_SU_EMAIL}', '${DJANGO_SU_PASSWD}')  " | python manage.py shell
fi

python manage.py runserver 0.0.0.0:8000
