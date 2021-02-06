from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
#from eralchemy import render_er

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return '<Contact %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            # do not serialize the password, its a security breach
        }

#####Recipe e Ingredent tienen una relación directa many-To-many por lo que hay
#####que usar una clase auxiliar que conecte ambas, de manera que:
#####la relación entre Recipe y la clase auxiliar sea one-To-many y
#####la relación entre la tabla auxiliar e Ingredent sea many-To-one.

# association_recipe_ingredient = Table('association_recipe_ingredient', db.metadata,
#     Column('ingredient_id', Integer, ForeignKey('ingredient.id')),
#     Column('recipe_id', Integer, ForeignKey('recipe.id'))
# )

# class Recipe(db.Model):

#     #__tablename__ = "recipe"

#     id = db.Column(db.Integer, primary_key=True)
#     recipe_name = db.Column(db.String(120), unique=False, nullable=False)
#     description = db.Column(db.String(800), unique=True, nullable=False)
#     img_url = db.Column(db.String(250), unique=True, nullable=False)
#     tags = db.Column(db.String(250), unique=False, nullable=False)
#     score= db.Column(db.Integer, unique=False, nullable=False)
#     ingredient_id = Column(Integer, ForeignKey("ingredient.id"), nullable=False)
   

#     def __repr__(self):
#         return '<Recipe %r>' % self.id

#     def serialize(self):
#         return {
#             "id": self.id,
#             "description": self.description,
#             "recipe_name": self.recipe_name,
#             "img_url": self.img_url,
#             "tags": self.tags,
#             "score": self.score,
#             "ingredient_id": self.ingredient_id,
            
            
#             # do not serialize the password, its a security breach
#         }

# class Ingredient(db.Model):

#     #__tablename__ = "ingredient"

#     id = db.Column(db.Integer, primary_key=True)
#     name_ingredient = db.Column(db.String(120), unique=True, nullable=False)
#     img_url = db.Column(db.String(250), unique=True, nullable=True)
#     recipe_id = Column(Integer, ForeignKey("recipe.id"), nullable=False)
#     ingredients = relationship("Recipe", secondary=association_recipe_ingredient)

#     def __repr__(self):
#         return '<Ingredient %r>' % self.id

#     def serialize(self):
#         return {
#             "id": self.id,
#             "name_ingredient": self.name_ingredient,
#             "img_url": self.img_url, 
#             "recipe_id": self.recipe_id,       
#             #"ingredient_recipe_id": self.ingredient_recipe_id,
#             # do not serialize the password, its a security breach
#         }
