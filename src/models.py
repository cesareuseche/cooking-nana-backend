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
        #self.salt= os.urandom(16).hex
        self.password_hash = self.set_password(password)
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
        
    def serializeUsername(self):
        return{
            'username' : self.username,
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
    score = db.Column(db.Integer, nullable=True)
    date_published = db.Column(db.DateTime(timezone=True), nullable=False)
    price = db.Column(db.Float, nullable=True)
    img_url = db.Column(db.String(250), nullable=False)
    ##la propiedad ingredients debe revisarse para que se relacione con otra tabla many-to-many
    #ingredients_received = db.relationship("Ingredient", backref="receiver", foreign_keys="Ingredient.recipes")
    ingredient = db.relationship("Recipeingredients", backref="recipe")

    def __init__(self, name, description, date_published, instructions, tags, likes, score, price, img_url, ingredient):
            self.name = name
            self.description = description
            self.date_published = datetime.now(timezone.utc)
            self.instructions = instructions
            self.tags = tags
            self.likes = likes
            self.score = score
            self.price = price
            #self.ingredients_received = ingredients_recived
            self.img_url = img_url
            self.ingredient = ingredient

    @classmethod
    def register(cls, name, description, date_published, instructions, tags, likes, score, price, img_url, ingredient):
        new_recipe = cls(
            name.lower(),
            description.lower(),
            date_published,
            instructions,
            tags,
            likes,
            score,
            price,
            #ingredients_received,
            img_url,
            ingredient
        )
        return new_recipe

    def serialize(self):
        #received_ingredients_list = self.ingredients_received
        #received_ingredients_list_serialize = list(map(lambda ingredient_list: ingredient_list.serialize(), received_ingredients_list))
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
            #'ingredients_recived' : self.received_ingredients_list_serialize,
            'img_url' : self.img_url,
            'ingredient' : self.ingredient
        }

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    category = db.Column(db.String(120), nullable=False)
    recipe = db.Column(db.Integer, db.ForeignKey("recipe.id"))
    #recipe = db.relationship("Recipe", secondary=Recipeingredients.__table__, lazy="select")

    def __init__(self, name, category, recipe):
            self.name = name
            self.category = category
            self.recipe = recipe

    def __repr__(self):
        return '<Ingredient %r>' % (self.name.title())

    @classmethod
    def register(cls, name, category, recipe):
        new_ingredient = cls(
            name.lower(), 
            category.lower(), 
            recipe,
        )
        return new_ingredient
    
    def serializeIngredient(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'category' : self.category,
            'recipe' : self.recipe,
        }


    def serialize(self):
        receiver = Recipe.query.get(self.recipe)
        return {
            'id' : self.id,
            'name' : self.name,
            'category' : self.category,
            'recipe' : self.recipe,
            'receiver' : receiver.name
        }

class Recipeingredients(db.Model):
    __tablename__ = 'recipeingredients'
    id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    ingredient = db.relationship("Ingredient", uselist=False)
    recipes = db.relationship("Recipe", uselist=False)
    units = db.Column(db.Numeric(4, 2))

    def __init__(self, ingredient=None, units=None):
        self.ingredient = ingredient
        self.units = units

    def __repr__(self):
        return '<Ingredient: %f units of %s>' % (self.units, self.ingredient.name)

    def serialize(self):
        return {
            'id' : self.id,
            'ingredient_id' : self.ingredient_id,
            'recipe_id' : self.recipe_id,
            'ingredient' : self.ingredient,
            'recipes' : self.recipes,
            'units' : self.units
        }