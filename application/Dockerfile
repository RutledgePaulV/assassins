FROM ubuntu:trusty
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y git
RUN apt-get install -y python3-dev
RUN apt-get install -y python3-setuptools
RUN apt-get install -y nodejs
RUN apt-get install -y npm
RUN apt-get install -y libpq-dev
RUN apt-get install -y libjpeg-dev
RUN apt-get install -y libpng-dev
RUN apt-get install -y supervisor
RUN easy_install3 pip
RUN pip3 install virtualenv
RUN npm install -g bower handlebars less grunt grunt-cli
RUN ln -s /usr/bin/nodejs /usr/bin/node
ENV PROJECT /opt/Assassins
RUN mkdir /opt/.env
RUN virtualenv /opt/.env
COPY ./Assassins/requirements.txt /opt/requirements.txt
RUN /opt/.env/bin/pip3 install -r /opt/requirements.txt
RUN /opt/.env/bin/pip3 install newrelic
COPY ./celery/* /etc/supervisor/conf.d/
COPY ./Assassins /opt/Assassins
RUN cd /opt/Assassins/static && bower install --allow-root
COPY ./scripts /opt/scripts
RUN chmod +x -R /opt/scripts
RUN /opt/.env/bin/python3 /opt/Assassins/manage.py collectstatic --noinput
WORKDIR /opt/Assassins