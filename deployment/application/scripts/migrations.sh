#!/bin/sh
/opt/.env/bin/python3 /opt/Assassins/Assassins/manage.py makemigrations
/opt/.env/bin/python3 /opt/Assassins/Assassins/manage.py migrate
/opt/.env/bin/python3 /opt/Assassins/Assassins/manage.py rebuild_index --noinput