#!/bin/bash

#restart this script as root, if not already root
[ `whoami` = root ] || exec sudo $0 $*

pip install -r requirements.txt
python TestProject/manage.py migrate
python TestProject/manage.py runserver 0.0.0.0:8000