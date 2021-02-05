from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Contact %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            # do not serialize the password, its a security breach
        }

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(800), unique=True, nullable=False)
    img_url = db.Column(db.String(250), unique=True, nullable=False)
    ingredient_1 = relationship("Ingredient", backref="Recipe")
    ingredient_2 = relationship("Ingredient", backref="Recipe")
    ingredient_3 = relationship("Ingredient", backref="Recipe")
    ingredient_4 = relationship("Ingredient", backref="Recipe")
    ingredient_5 = relationship("Ingredient", backref="Recipe")
    ingredient_6 = relationship("Ingredient", backref="Recipe")
    ingredient_7 = relationship("Ingredient", backref="Recipe")
    ingredient_8 = relationship("Ingredient", backref="Recipe")
    ingredient_9 = relationship("Ingredient", backref="Recipe")
    ingredient_10 = relationship("Ingredient", backref="Recipe")

    def __repr__(self):
        return '<Recipe %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "recipe_name": self.recipe_name,
            "img_url": self.img_url,
            "ingredient_1": self.ingredient_1,
            "ingredient_2": self.ingredient_2,
            "ingredient_3": self.ingredient_3,
            "ingredient_4": self.ingredient_4,
            "ingredient_5": self.ingredient_5,
            "ingredient_6": self.ingredient_6,
            "ingredient_7": self.ingredient_7,
            "ingredient_8": self.ingredient_8,
            "ingredient_9": self.ingredient_9,
            "ingredient_10": self.ingredient_10,
            # do not serialize the password, its a security breach
        }

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_ingredient = db.Column(db.String(120), unique=False, nullable=True)
    img_url = db.Column(db.String(250), unique=True, nullable=True)
    recipe_id = db.Column(Integer, ForeignKey('Recipe.id'))
    recipe = relationship(Recipe)

    def __repr__(self):
        return '<Recipe %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "recipe_name": self.recipe_name,
            "img_url": self.img_url,
            "ingredients": self.ingredients,
            "recipe_id": self.recipe_id,
            # do not serialize the password, its a security breach
        }