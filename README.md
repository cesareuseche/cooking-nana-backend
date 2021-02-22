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

-Need to install: `python3 -m pip install flask-jwt-extended`

`pipenv install flask-jwt-extended`

`pip3 install requests`

`python3 -m pip install pandas`

`python3 -m pip install requests`

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

# TO USE THIS API 

## Endpoint:

### Edit tables

    Enter in mySQL with: mysql -h localhost -u your_user

    drop database contact;
    create database contact;    (remember pipenv run migrate and pipenv run upgrade after create)
    use contact;
    show tables;
    ALTER TABLE recipeingredients MODIFY id int NOT NULL AUTO_INCREMENT; (parece ya no ser necesario este paso)
    exit

### /register

    This is a POST endpoint, so you will need:
    {
        "email":"email@example.com",
        "name":"aName",
        "last_name":"aLastName",
        "username":"some_user",
        "password":"notEasy123"
    }

    then, if everything is correct, server will respond:
    {
        "email": "email@example.com",
        "id": 1,
        "last_name": "alastname",
        "name": "aname",
        "status": true,
        "username": "some_user"
    }

### /users

    This is a GET endpoint, you will obtain a list o all users

### /user/<int:position>

    This is a GET endpoint, you will need enter the user id to obtain data

### /login
    You need copy to your .env file the APP_JWT_SECRET LINE (with versión jwt extended, use this lib: create_access_token)

    This is a POST endpoint, enter data as:
    {
        "username":"some_user",
        "password":"notEasy123"
    }

    or this way works too:
    {
        "email": "email@example.com",
        "password":"notEasy123"
    }

    if everything is allright you will get:
    {
        "email": "email@example.com",
        "id": 1,
        "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTI5MDg1MDYsIm5iZiI6MTYxMjkwODUwNiwianRpIjoiNTNlM2RiOTgtYjI0Ni00NWFkLWFkOTMtOTUxZTZhMDY0ODUzIiwiZXhwIjoxNjEyOTA5NDA2LCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIiwiY3NyZiI6ImJlOTkzNDE5LWRiZjgtNGQ4MC1hMTVlLWM0OGQyOGJjNGY0NyJ9.s88fi9FzIMWE7AyYRfwDDc-jottegqeMatscAMjr9B0",
        "last_name": "alastname",
        "name": "aname",
        "status": true,
        "username": "some_user"
    }

### /check
    This is a GET endpoint, it will retrieve Authorization.
    For that you must enter jwt generated Token at login endpoint, as Bearer Token on HEADER.

    Example:
    
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTI5MDg1MDYsIm5iZiI6MTYxMjkwODUwNiwianRpIjoiNTNlM2RiOTgtYjI0Ni00NWFkLWFkOTMtOTUxZTZhMDY0ODUzIiwiZXhwIjoxNjEyOTA5NDA2LCJpZGVudGl0eSI6MSwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIiwiY3NyZiI6ImJlOTkzNDE5LWRiZjgtNGQ4MC1hMTVlLWM0OGQyOGJjNGY0NyJ9.s88fi9FzIMWE7AyYRfwDDc-jottegqeMatscAMjr9B0

    if everything is ok, you will get:

    {
    "msg": "Welcome, <Contact 'some_user'>"
    }

### /ingredients

    This could be used as GET endpoint, you will obtain a list o all ingredients.

    When this endpoint is used with POST method will be acting automatically inside of
    /recipes endpoint

### /recipes

    This could be used as GET endpoint, you will obtain a list o all recipes.

    When this endpoint is used with POST method, data should be as:

    {
    "description":"Description of the recipe",
    "name":"Name of recipe",
    "instructions":"Some instructions of how to cook",
    "tags":"tags will help to find recipe",
  	"img_url":"test",
  	"ingredients":"['onion', 'potato']",
  	"date_published":"2021-02-20T14:04"
    }

    It will create necesary ingredients of recipes automatically.

    At the moment, response body will be something like:

    [
        {
        "date_published": ["Sat, 20 Feb 2021 14:04:00 GMT"],
        "description": ["description of the recipe3"],
        "id": [3],
        "img_url": ["test"],
        "ingredients_used": "['onion', 'potato', 'rice', 'tomato']",
        "instructions": ["Some instructions of how to cook"],
        "likes": [0],
        "name": ["name of recipe3"],
        "price": [99.99],
        "score": [9],
        "tags": ["tags will help to find recipe"]
        }
    ]

### /recipes/<int:position>

    This is a GET endpoint, you will need enter the recipe id to obtain data

    {
    "date_published": "Sat, 20 Feb 2021 14:04:00 GMT", 
    "description": "description of the recipe3", 
    "id": 3, 
    "img_url": "test", 
    "ingredients_used": "['onion', 'potato', 'rice', 'tomato']", 
    "instructions": "Some instructions of how to cook", 
    "likes": 0, 
    "name": "name of recipe3", 
    "price": 99.99, 
    "score": 9, 
    "tags": "tags will help to find recipe"
    }

### /search

    This is a POST endpoint, you will need enter the ingredients name (no matter if uppercase, or lowercase) to obtain ID of recipes where those ingredients are beeing used.

    {
	"search": "['rice', 'arugula']"   
    }

    if everything is correct, you will get:

    {
    "response": [
                    [1,2,3],
                    [4]
                ]
    }

    After that, you can use /recipes/<int:position> endpoint to obtain the specific recipe
## Other

### Script to populate database automatically for test (DATABASE MUST BE EMPTY)
    
    To run this test, just navigate to folder: ./src/  
    Then apply this command:

    `python dataAuto.py`

    it will send 20 recipes with random ingredients to /recipes endpoint.
    Could take some time.

### [🙎‍♂️ About us]

We are making this API as part of back-end of our final 4Geeks Academy Fullstack course project.
    
In alphabetical order:

[Becerra, Humberto](https://github.com/humbi-exe) /
[Martínez, Antonio](https://github.com/metantonio) /
[Pérez, Vincent](https://github.com/vinsh15) /
[Useche, César](https://github.com/cesareuseche) /

<p align="center">
  <a href="https://github.com/vinsh15/backend-prototype">
    <img src="https://github.com/cesareuseche/cooking-nana-frontend/blob/master/src/img/logo.png" alt="Cooking-nana" width="100px" />
  </a>
</p>

<p align="center">
  <a href="https://github.com/cesareuseche/cooking-nana-frontend">
    <img src="https://img.shields.io/website?down_message=down&up_color=green&up_message=online&url=https%3A%2F%2Fsupercookie.me" alt="Front-End">
  </a>
  <a href="https://github.com/vinsh15/backend-prototype">
    <img src="https://img.shields.io/github/license/jonasstrehle/supercookie" alt="License">
  </a>
</p>
