# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add bash
ADD requirements.txt startup.sh /code/
WORKDIR /code
#CMD ["pip", "install", "-r", "/requirements.txt"]
ADD ./TestProject /code/TestProject
ADD ./app /code/app
ADD ./manage.py /code/manage.py