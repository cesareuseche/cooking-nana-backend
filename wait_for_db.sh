#!/bin/sh
echo "waiting for mysql to be ready..."

while ! nc -z example_db 3306 ; do sleep 10 ; done ;

echo "mysql started..."

pipenv run init

echo "running migrations..."

pipenv run migrate

echo "upgrading db..."

pipenv run upgrade

echo "db ready... launching app"

pipenv run start