# syntax=docker/dockerfile:1
FROM python:3.10-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY TestProject/requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/