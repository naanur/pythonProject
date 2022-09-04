# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
ADD requirements.txt startup.sh /code/

RUN python3 -m pip install --upgrade pip
RUN ["/usr/bin/pip", "install", "-r", "/requirements.txt"]
RUN apk update && apk add bash

ADD ./TestProject /code/TestProject
ADD ./app /code/app
ADD ./manage.py /code/manage.py