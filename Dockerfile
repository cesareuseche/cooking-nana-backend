FROM python:3.8-alpine

COPY ./Pipfile ./Pipfile.lock /app/
USER root
WORKDIR /app

RUN apk add build-base mariadb-dev mariadb-client postgresql-dev

RUN pip install pipenv

RUN pipenv install

COPY . /app/
EXPOSE 3000