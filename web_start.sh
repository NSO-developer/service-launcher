#!/bin/bash

# creates passwd file to be able to ssh and scp from openshift.

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
envsubst < /root/passwd.template > /usr/src/app/web_ui/data/passwd
export LD_PRELOAD=libnss_wrapper.so
export NSS_WRAPPER_PASSWD=/usr/src/app/web_ui/data/passwd
export NSS_WRAPPER_GROUP=/etc/group

# Get current directory


# Set up any db change
python /usr/src/app/manage.py makemigrations

# Updates/Creates Database
python /usr/src/app/manage.py migrate

# Starts server
python /usr/src/app/manage.py runserver 0.0.0.0:8025