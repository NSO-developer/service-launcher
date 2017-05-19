#!/bin/bash
pip install -r requirements.txt
# Set up any db change
python manage.py makemigrations

# Updates/Creates Database
python manage.py migrate

# Starts server
python manage.py runserver 0.0.0.0:8025