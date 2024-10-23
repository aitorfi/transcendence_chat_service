#!/bin/bash

sleep 5

python manage.py makemigrations chat
python manage.py migrate

python3 -m daphne -b 0.0.0.0 -p 8080 chat_service.asgi:application
