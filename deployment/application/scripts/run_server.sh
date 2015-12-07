#!/bin/sh

# generate new relic config
/opt/.env/bin/newrelic-admin generate-config ${NEW_RELIC_LICENSE_KEY} ${NEW_RELIC_CONFIG_FILE}

# start celery
supervisord

# finally, end with starting the application
exec /opt/.env/bin/newrelic-admin run-program /opt/.env/bin/gunicorn Assassins.wsgi:application -w ${GUNICORN_WORKERS} -b unix:${GUNICORN_SOCKET}