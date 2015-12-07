#!/bin/sh

# generate new relic config
/opt/.env/bin/newrelic-admin generate-config ${NEW_RELIC_LICENSE_KEY} ${NEW_RELIC_CONFIG_FILE}

# run data migrations
/opt/.env/bin/python3 /opt/Assassins/manage.py makemigrations
/opt/.env/bin/python3 /opt/Assassins/manage.py migrate
/opt/.env/bin/python3 /opt/Assassins/manage.py rebuild_index --noinput

# start celery
supervisord

# finally, end with starting the application
exec /opt/.env/bin/newrelic-admin run-program /opt/.env/bin/gunicorn Assassins.wsgi:application -w 3 -b unix:/opt/sockets/gunicorn.sock