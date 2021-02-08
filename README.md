# Flask Boilerplate for Profesional Development

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/from-referrer/)
<p align="center">
    <a href="https://youtu.be/ORxQ-K3BzQA"><img height="200px" src="https://github.com/4GeeksAcademy/flask-rest-hello/blob/master/docs/assets/how-to.png?raw=true" /></a>
</p>

## Features

- Extensive documentation [here](https://github.com/4GeeksAcademy/flask-rest-hello/tree/master/docs).
- Integrated with Pipenv for package managing.
- Fast deloyment to heroku with `$ pipenv run deploy`.
- Use of `.env` file.
- SQLAlchemy integration for database abstraction.

## Installation (automatic if you are using gitpod)

> Important: The boiplerplate is made for python 3.7 but you can easily change the `python_version` on the Pipfile.

The following steps are automatically runned withing gitpod, if you are doing a local installation you have to do them manually:

-Need to install: `python3 -m pip install flask-jwt-simple`

```sh
pipenv install;
mysql -u root -e "CREATE DATABASE example";
pipenv run start;
pipenv run init;
pipenv run migrate;
pipenv run upgrade;
```

## How to Start coding?

There is an example API working with an example database. All your application code should be written inside the `./src/` folder.

- src/main.py (it's where your endpoints should be coded)
- src/models.py (your database tables and serialization logic)
- src/utils.py (some reusable classes and functions)
- src/admin.py (add your models to the admin and manage your data easily)

For a more detailed explanation, look for the tutorial inside the `docs` folder.

## Remember to migrate every time you change your models

You have to migrate and upgrade the migrations for every update you make to your models:
```
$ pipenv run migrate (to make the migrations)
$ pipenv run upgrade  (to update your databse with the migrations)
```


# Manual Installation for Ubuntu & Mac

⚠️ Make sure you have `python 3.6+` and `MySQL` installed on your computer and MySQL is running, then run the following commands:
```sh
$ pipenv install (to install pip packages)
$ pipenv run migrate (to create the database)
$ pipenv run start (to start the flask webserver)
```

# Launch using docker

1. ⚠️ If you don't have docker installed on your computer, please go [get docker](https://docs.docker.com/get-docker/)
2. ⚠️ If on linux, install docker-compose following [these instructions](https://docs.docker.com/compose/install/)
3. Clone the repo and create a `.env` file; complete key-value pairs as proposed on `.env.example` file
4. Run `docker-compose up` and give it a few minutes
5. Have some coffee (Really large coffee)
5.1 Delete Migration
6. Your mysql service should be up on port 33060 (from host, a.k.a. your OS)
7. Your api service should be up on port 3000 (from host, also your OS)
8. Go to Docker Desktop, run flask-rest-hello and run cli
9. Run on terminal: `mysql`
10. Now you can use commands as: `show databases;`   `use example;`   `show tables;` `create database NameOfDB;` `drop database NameOfDB; describe contact;`

## Deploy to Heroku

This template is 100% compatible with Heroku[https://www.heroku.com/], just make sure to understand and execute the following steps:

```sh
// Install heroku
$ npm i heroku -g
// Login to heroku on the command line
$ heroku login -i
// Create an application (if you don't have it already)
$ heroku create <your_application_name>
// Commit and push to heroku (commited your changes)
$ git push heroku master
```
:warning: For a more detailed explanation on working with .env variables or the MySQL database [read the full guide](https://github.com/4GeeksAcademy/flask-rest-hello/blob/master/docs/DEPLOY_YOUR_APP.md).

## Implementing changes in database

1. `pipenv run migrate` to implement change on Database tables at models.py to folder Migration
2. `pipenv run upgrade` to update database with changes.

## To solve FATAL ERROR on pre-production

1. Just eliminate folder migration.
2. 1. For docker users only have to use `docker-compose up --build`
2. 2. Go to project in docker and run terminal `pipenv run init` `pipenv run migrate` `pipenv run upgrade`, then open mysql terminal on docker and run: `drop database example;` and `create database example;` 

## To solve FATAL ERROR on final production

1. Try to save database, DO NOT delete migration folder
2. Read /docs