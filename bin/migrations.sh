#!/bin/bash

docker compose exec backend bash -c 'python manage.py makemigrations && python manage.py migrate'
