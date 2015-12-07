# base it on ubuntu 14
from ubuntu:trusty


# setup the operating system with required packages
RUN apt-get update
RUN apt-get install -y build-essential git python3-dev python3-setuptools nodejs npm libpq-dev libjpeg-dev libpng-dev
RUN easy_install3 pip
RUN pip3 install virtualenv
RUN npm install -g bower handlebars less grunt grunt-cli
RUN apt-get -y upgrade
RUN ln -s /usr/bin/nodejs /usr/bin/node
ENV PROJECT /opt/Assassins/Assassins

# prepare the virtualenv
RUN mkdir /opt/.env
RUN virtualenv /opt/.env


# setup to read from github repositories
RUN mkdir /root/.ssh/
ADD id_rsa /root/.ssh/id_rsa
RUN chmod -R 600 /root/.ssh
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts


# we keep a base set of requirements in the dockerfile
# so that we don't bust the whole pip cache
# on every project update
COPY ./requirements.txt /opt/requirements.txt
RUN /opt/.env/bin/pip3 install -r /opt/requirements.txt
RUN /opt/.env/bin/pip3 install newrelic


# install supervisor
# copy celery scripts and config
RUN apt-get install -y supervisor
COPY ./celery/* /etc/supervisor/conf.d/


# clone the project and install specific packages
ENV ASSASSINS_COMMIT e1ab92b3b1cf678c6c57f461a3f8a3a9139d0c82
RUN git clone git@github.com:RutledgePaulV/Assassins.git /opt/Assassins
RUN cd /opt/Assassins && git checkout ${ASSASSINS_COMMIT}
RUN /opt/.env/bin/pip3 install -r ${PROJECT}/requirements.txt
RUN cd ${PROJECT}/static && bower install --allow-root


# copy shell scripts
COPY ./scripts /opt/scripts
RUN chmod +x -R /opt/scripts


WORKDIR ${PROJECT}