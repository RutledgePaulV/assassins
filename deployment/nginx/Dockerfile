FROM tutum/nginx

# remove the default config
RUN rm /etc/nginx/sites-enabled/default

# copy site config and error pages over
COPY error-pages/ /etc/nginx/error-pages
COPY sites-enabled/ /etc/nginx/sites-enabled

COPY ./keys/nginx_signing.key /opt/nginx_signing.key
RUN apt-key add /opt/nginx_signing.key

RUN echo "deb http://nginx.org/packages/ubuntu/ trusty nginx" | tee -a /etc/apt/sources.list
RUN echo "deb-src http://nginx.org/packages/ubuntu/ trusty nginx" | tee -a /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y nginx-nr-agent crudini apache2-utils

COPY ./scripts /opt/scripts
RUN chmod +x -R /opt/scripts

# create a user for basic auth on flower
RUN htpasswd -bc /etc/nginx/.htpasswd admin flowerpetals