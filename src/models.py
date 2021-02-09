from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from base64 import b64encode
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import os
import json

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    salt = db.Column(db.String(16), nullable=False)
    status = db.Column(db.Boolean(), nullable=False)

    #aca va el relationship con otra tabla del tipo many-to many

    def __init__(self, email, name, last_name, username, password, status):
        self.email = email
        self.name = name
        self.last_name = last_name
        self.username = username
        self.salt = b64encode(os.urandom(4)).decode("utf-8")
        self.set_password(password)
        self.status = status
    
    def set_password (self, password):
        self.password_hash = generate_password_hash(f"{password}{self.salt}")
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, f"{password}{self.salt}")

    @classmethod
    def register(cls, email, name, last_name, username, password):
        new_user = cls(
            email, 
            name.lower(), 
            last_name.lower(),
            #100, 
            username, 
            password, 
            True
        )
        return new_user


    def __repr__(self):
        return '<Contact %r>' % self.username

    def serializeUsers(self):
        return{
            'id' : self.id,
            'username' : self.username,
            'status' : self.status,
            'email': self.email
        }
        

    def serialize(self):
        return {
            'id' : self.id,
            'email' : self.email,
            'name' : self.name,
            'last_name' : self.last_name,
            'username' : self.username,
            'status' : self.status,
        }

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000), unique=False, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    instructions = db.Column(db.String(1000), unique=False, nullable=False)
    tags = db.Column(db.String(250), nullable=False)
    likes = db.Column(db.Integer, nullable=True)
    score = db.Column(db.Integer, nullable=False)
    date_published = db.Column(db.DateTime(timezone=True), nullable=False)
    price = db.Column(db.Float, nullable=True)
    img_url = db.Column(db.String(250), nullable=False)
    ##la propiedad ingredients debe revisarse para que se relacione con otra tabla many-to-many
    ingredients_received = db.relationship("Ingredient", backref="receiver", foreign_keys="Ingredient.recipes")

    def __init__(self, name, description, date_published, instructions, tags, likes, score, price, ingredients, img_url):
            self.name = name
            self.description = description
            self.date_published = datetime.now(timezone.utc)
            self.instructions = instructions
            self.tags = tags
            self.likes = likes
            self.score = score
            self.price = price
            self.ingredients_received = ingredients_recived
            self.img_url = img_url

    @classmethod
    def register(cls, name, description, date_published, instructions, tags, likes, score, price, ingredients_received, img_url):
        new_recipe = cls(
            name.lower(),
            description.lower(),
            date_published,
            instructions,
            tags,
            likes,
            score,
            price,
            ingredients_received,
            img_url
        )
        return new_recipe

    def serialize(self):
        received_ingredients_list = self.ingredients_received
        received_ingredients_list_serialize = list(map(lambda ingredient_list: ingredient_list.serialize(), received_ingredients_list))
        return {
            'id' : self.id,
            'name' : self.name,
            'description' : self.description,
            'date_published' : self.date_published,
            'instructions' : self.instructions,
            'tags' : self.tags,
            'likes' : self.likes,
            'score': self.score,
            'price': self.price,
            'ingredients_recived' : self.received_ingredients_list_serialize,
            'img_url' : self.img_url,
        }

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    category = db.Column(db.String(120), nullable=False)
    recipes = db.Column(db.Integer, db.ForeignKey("recipe.id"))

    def __init__(self, name, category, recipes):
            self.name = name
            self.category = category
            self.recipes = recipes

    @classmethod
    def create_ingredient(cls, name, category, recipes):
        new_ingredient = cls(
            name.lower(), 
            category.lower(), 
            recipes,
        )
        return new_ingredient
    
    def serializeIngredient(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'category' : self.category,
            'recipes' : self.recipes,
        }


    def serialize(self):
        receiver = Recipe.query.get(self.recipes)
        return {
            'id' : self.id,
            'name' : self.name,
            'category' : self.category,
            'recipes' : self.recipes,
            'receiver' : receiver.name
        }