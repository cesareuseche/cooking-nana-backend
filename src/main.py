"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, threading
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Contact, Recipe, Ingredient, Recipeingredients
from flask_jwt_extended import (
JWTManager, jwt_required, create_access_token, get_jwt_identity
)
from werkzeug.security import safe_str_cmp, generate_password_hash, check_password_hash
from datetime import datetime
import json
from io import StringIO
from ast import literal_eval
import re

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get("APP_JWT_SECRET") #Aquí se cambia la configuración de JWT
#app.config['JWT_SECRET_KEY'] = 'test'
app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']
MIGRATE = Migrate(app, db)
db.init_app(app)
jwt = JWTManager(app) #JSON web tokens para autenticación en el servidor
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#A diferencia de obtener una lista de contactos
#ahora la meta es verificar cada usuario que hace login de 
#manera individual coincida su password con username
@app.route('/user', methods=['GET'])
@jwt_required
def get_user():
    user = Contact.query.get(get_jwt_identity()) #parecido al query.all() pero con la finalidad de obtener los tokens jwt
    #response_body = [] #No es necesario porque no se obtendrá una lista de usuarios
    if isinstance(user, Contact):
        return jsonify(user.serialize())
    else:
        return jsonify({
            "result": "user doesn't exist"
        }),400

#Por otro lado, si como administradores quisieramos obtener
#toda la lista de usuarios en la base de datos, haríamos
#otro método Get con un nuevo end-point.
@app.route('/users', methods=['GET'])
def get_users():
    """ buscar y regresar todos los usuarios """
    users = Contact.query.all()
    users_serialize = list(map(lambda user: user.serializeUsers(), users)) #serializeUser() se definició como función dentro de la clase Contact
    return jsonify(users_serialize), 200

#Otra cosa que podríamos querer es 
#la información de un usuario en particular
@app.route('/user/<user_id>', methods=['GET'])
def get_user_id(user_id):
    """ buscar y regresar un usuario en especifico """
    user = Contact.query.get(user_id)
    if isinstance(user, Contact):
        return jsonify(user.serialize()), 200
    else:
        return jsonify({
            "result": "user not found"
        }), 404

#La forma de registrar al usuario debe ser con un método
#POST con un end-point relacionado con el front-end
#como por ejemplo el end-point /register
@app.route('/register', methods=['POST'])
def post_user():
    """
        "POST": registrar un usuario y devolverlo
    """
    body = request.json
    print(request.get_json())
    if body is None:
        return jsonify({
            "response": "empty body"
        }), 400

    if (
        "email" not in body or
        "name" not in body or
        "last_name" not in body or
        "username" not in body or
        "password" not in body 
    ):
        return jsonify({
            "response": "Missing properties"
        }), 400
    if(
        body["email"] == "" or
        body["name"] == "" or
        body["last_name"] == "" or
        body["username"] == "" or
        body["password"] == ""
    ):
        return jsonify({
            "response": "empty property values"
        }), 400

    new_user = Contact.register(
        body["email"],
        body["name"],
        body["last_name"],
        body["username"],
        body["password"],
        
    )
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify(new_user.serialize()), 201
    except Exception as error:
        db.session.rollback()
        print(f"{error.args} {type(error)}")
        return jsonify({
            "response": f"{error.args}"
        }), 500

#Ahora vendría un end-point del tipo POST
#para cuando el usuario introduce su usuario y password
@app.route("/login", methods=["POST"])
def handle_login():
    """ Compara El usuario/correo con la base de datos y genera un token si hay match """

    request_body = request.json

    if request_body is None:
        return jsonify({
            "result" : "missing request body"

        }), 400

    if (
        ("email" not in request_body and "username" not in request_body ) or
        "password" not in request_body
    ):
        return jsonify({
            "result": "missing fields in request body"
        }), 400


    jwt_identity = ""

    user = None

    if "email" in request_body: 
        jwt_identity = request_body["email"]
        user = Contact.query.filter_by(email=request_body["email"]).first()
    else:
        jwt_identity = request_body["username"]
        user = Contact.query.filter_by(username=request_body["username"]).first()


    ret = None

    if isinstance(user, Contact):
        if (user.check_password(request_body["password"])):
            jwt = create_access_token(identity = user.id)
            ret = user.serialize()
            ret["jwt"] = jwt
        else: 
            return jsonify({
                "result": "invalid data"
            }), 400
    else:
        return jsonify({
                "result": "user not found"
            }), 404
                    
            
    return jsonify(ret), 200

@app.route("/ingredients", methods=["GET"])
def get_ingredients():
    ingredients = Ingredient.query.all()
    ingredients_serialize = list(map(lambda ingredient: ingredient.serialize(), ingredients)) 
    return jsonify(ingredients_serialize), 200

@app.route("/ingredients", methods=["POST"])
def post_ingredients():
    """
        "POST": registrar un ingrediente
    """
    request_body = request.json

    if request_body is None:
        return jsonify({
            "response": "empty body"
        }), 400

    if("name" not in request_body   or
        "category" not in request_body
    ):
        return jsonify({
            "result": "missing fields in request body"
        }), 400

    if(
        request_body["name"] == "" or
        request_body["category"] == ""
    ):
        return jsonify({
            "response": "empty property values"
        }), 400

    new_ingredient = Ingredient.register(
        request_body["name"],
        request_body["category"],        
    )
    db.session.add(new_ingredient)
    try:
        db.session.commit()
        return jsonify(new_ingredient.serializeIngredient()), 201
    except Exception as error:
        db.session.rollback()
        print(f"{error.args} {type(error)}")
        return jsonify({
            "response": f"{error.args}"
        }), 500

@app.route("/check")
@jwt_required
def handle_check():
    id_of_user = get_jwt_identity()
    user = Contact.query.get(id_of_user)
    return jsonify({"msg":f"Welcome, {user}"})


@app.route('/recipes', methods=['GET'])
def get_recipes():
    """ buscar y regresar todos las recetas """
    recipes = Recipe.query.all()
    recipes_serialize = list(map(lambda recipe: recipe.serialize(), recipes))
    return jsonify(recipes_serialize), 200

@app.route('/recipes/<recipe_id>', methods=['GET'])
def get_recipe_id(user_id):
    """ buscar y regresar una receta en especifico """
    recipe = Recipe.query.get(recipe_id)
    if isinstance(recipe, Recipe):
        return jsonify(recipe.serialize()), 200
    else:
        return jsonify({
            "result": "user not found"
        }), 404


##Se definirá una función de búsqueda, qué según el id de un ingrediente
##devuelva una lista con los id de las recetas asociadas:
def get_id_Recipes_from_Ingredient_id(ingredient_ids):
    return Recipe.query.\
        join(Recipeingredients).\
        filter(Recipeingredients.ingredient_id.in_(ingredient_ids)).\
        group_by(Recipe.id).\
        having(db.func.count(Recipeingredients.ingredient_id.distinct()) ==
               len(set(ingredient_ids))).\
        all()


@app.route('/recipes', methods=['POST'])
def post_recipe():
    """
        "POST": registrar un usuario y devolverlo
    """
    body = request.json
    if body is None:
        return jsonify({
            "response": "empty body"
        }), 400

    if (
        "description" not in body or
        "name" not in body or
        "instructions" not in body or
        "tags" not in body or
        "img_url" not in body 
    ):
        return jsonify({
            "response": "Missing properties"
        }), 400
    if(
        body["description"] == "" or
        body["name"] == "" or
        body["instructions"] == "" or
        body["tags"] == "" or
        body["img_url"] == ""
    ):
        return jsonify({
            "response": "empty property values"
        }), 400

    obtained_ingredients_id=[]
    ingredients_body=[]
    ingredients_body = json.dumps(request.json["ingredients"])
    ingredients_body = literal_eval(ingredients_body)
    
    #print(type (ingredients_body))
    # Converting string to list 
    ingredients_body = ingredients_body.strip('][').split(', ')

    recipe=[]
    for individual_ingredient in ingredients_body:
        
        #print(f'este es el for individdual {individual_ingredient}')
        #recipe.append(new_recipe_id)
        category="a"
        match = db.session.query(Ingredient.name).filter_by(name=individual_ingredient).first()
        print(f'esto sería el match {match} y el ingredient {individual_ingredient}')

        new_ingredient = Ingredient.register(
            individual_ingredient,
            "none",
            recipe        
        )
        db.session.add(new_ingredient)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
    ################################Hasta este punto está funcionando




    #print(type (ingredients_body))
    for individual_ingredient in ingredients_body:
        print(type (individual_ingredient))
        print(individual_ingredient)
        #Para obtener el id del ingrediente si el nombre del mismo aparece en el body    
        match = db.session.query(Ingredient.id).filter_by(name=individual_ingredient).first()
        print(f'esto sería el match {match}')
        print(type(match))
        obtained_ingredients_id.append(match)
        #con el ejemplo los ID obtenidos vienen como listas, pero siguiente formato [(1,),(2,)], hay que arregarlo

    print(f'esta sería obtained_id {obtained_ingredients_id}')
    print(type(obtained_ingredients_id))
    string_ingredient_id="".join(map(str, obtained_ingredients_id))
    #print(f'esta sería como cadena{string_ingredient_id}')
    string_ingredient_id = string_ingredient_id.strip('()')
    string_ingredient_id = string_ingredient_id.replace(')(',"")
    string_ingredient_id = string_ingredient_id.replace(')',"")
    if(string_ingredient_id[-1]==","):
        string_ingredient_id=string_ingredient_id.rstrip(string_ingredient_id[-1])
    #print(f'esta sería como cadena recortada {string_ingredient_id}') ##en este punto los id quedan: 1,2
    string_ingredient_id="["+string_ingredient_id+"]"
    print(f'esta sería como cadena string {string_ingredient_id}') ##en este punto los id quedan [1,2] pero strings
    #string_ingredient_id = list(map(int, string_ingredient_id))
    string_ingredient_id=literal_eval(str(string_ingredient_id))
    print(f'esta sería como lista enteros {string_ingredient_id}') ##en este punto devuelve como lista de enteros
    print(type(string_ingredient_id))
    #print(body["ingredients"])        
    body["ingredients"] = string_ingredient_id     ####hasta aquí está bien, devolvió lista id de onion y potato
 
    #ya teniendo la lista de los ID de los ingredientes, faltaría el ID del recipe que estamos por crear, para
    #meterlo en la tabla relacional, y después de eso, poder registrar el Recipe correctamente.
    if(db.session.query(Recipe).order_by(Recipe.id.desc()).first()):
        last_recipe_id = db.session.query(Recipe).order_by(Recipe.id.desc()).first()
        last_recipe_id=(last_recipe_id.id)
        new_recipe_id = 1+last_recipe_id
    else: 
        last_recipe_id = 0
        new_recipe_id = 1
    # #print(f'Este es el último id registrado {last_recipe_id}') #devuelve <Recipe 1>
    # #print(type(last_recipe_id)) #es del tipo models.Recipe
    # last_recipe_id=(last_recipe_id.id)
    # #print(f'Este es el último id registrado {last_recipe_id}')
    # #print(type(last_recipe_id)) #es del tipo entero!!
    # new_recipe_id = 1+last_recipe_id
    # #print(new_recipe_id)

    #Suponemos que del body llega una lista [onion, potato] de ingredientes, tal que:
    #ingredients_body = body["ingredients"]
    ####################################################################################
    

    ##Ya teniendo el ID del nuevo recipe a crear y la lista de ID de ingredientes, es hora de registrar en
    ## la tabla de clase relaciona Recipeingredients
    integer_ingredient_id=string_ingredient_id # it's a List
    print(f'This is integer_ingredient_id {integer_ingredient_id} and type:')
    print(type(integer_ingredient_id))
   
    empty_list=[]
    ##Registro del nuevo Recipe
    new_list_ingredients=[]
    new_recipe = Recipe.register(
        body["name"],
        body["description"],
        body["date_published"],
        body["instructions"],
        body["tags"],
        #body["price"],
        #body["score"],
        body["img_url"],
        empty_list #but integer or may be sqlalchemy object 
    )
    db.session.add(new_recipe)
    db.session.commit()
    
    recipe_id_list=[]
    ingredients_list=[]

    #Registro clase intermedia Recipeingredients######################################
    for counter in integer_ingredient_id:
        new_relationship = Recipeingredients.register(
            counter,
            new_recipe_id
        )
        print(type(counter))
        db.session.add(new_relationship)
        db.session.commit()
        # try:
        #     return db.session.commit()
        # except Exception as error:
        #     db.session.rollback()
        #     print(f"{error.args} {type(error)}")
    #################################################################################


    try:
        db.session.commit()
        return jsonify(new_recipe.serialize()), 201
    except Exception as error:
        db.session.rollback()
        print(f"{error.args} {type(error)}")
        return jsonify({
            "response": f"{error.args}"
        }), 500

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=PORT, debug=False)
