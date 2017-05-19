#!/bin/bash

# creates passwd file to be able to ssh and scp

export USER_ID=$(id -u) 
export GROUP_ID=$(id -g)
envsubst < /root/passwd.template > /usr/src/app/web_ui/nso_data/passwd
export LD_PRELOAD=libnss_wrapper.so
export NSS_WRAPPER_PASSWD=/tmp/passwd
export NSS_WRAPPER_GROUP=/etc/group

# Set up any db change
python manage.py makemigrations

# Updates/Creates Database
python manage.py migrate

# Starts server
python /usr/src/app/manage.py runserver 0.0.0.0:8025