#!/bin/sh
crudini --set /etc/nginx-nr-agent/nginx-nr-agent.ini global newrelic_license_key ${NEW_RELIC_LICENSE_KEY}
crudini --set /etc/nginx-nr-agent/nginx-nr-agent.ini source1 name ${NEW_RELIC_NGINX_NAME}
crudini --set /etc/nginx-nr-agent/nginx-nr-agent.ini source1 url ${NEW_RELIC_NGINX_STATUS_URL}
service nginx-nr-agent start