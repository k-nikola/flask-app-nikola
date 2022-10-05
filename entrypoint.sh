#!/bin/bash

mkdir -p /var/log/flaskapp
touch /var/log/flaskapp/error.log
touch /var/log/flaskapp/access.log

exec gunicorn webapp:app --name flask-app-nikola \
--bind 0.0.0.0:5000 \
--workers 3 \
--log-level=info \
--log-file=/var/log/flaskapp/error.log \
--access-logfile=/var/log/flaskapp/access.log \
