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
from models import db, Contact#, Recipe, Ingredient
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get("APP_JWT_SECRET")
MIGRATE = Migrate(app, db)
db.init_app(app)
jwt = JWTManager(app) #JSON web tokens to verify authorization of our server
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
#manera individual
@app.route('/contact', methods=['GET'])
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
@app.route('/contacts', methods=['GET'])
def get_users():
    """ buscar y regresar todos los usuarios """
    users = Contact.query.all()
    users_serialize = list(map(lambda user: user.serializeUsers(), users))
    return jsonify(users_serialize), 200

#Otra cosa que podríamos querer es 
#la información de un usuario en particular
@app.route('/contact/<user_id>', methods=['GET'])
def get_user_id(user_id):
    """ buscar y regresar un usuario en especifico """
    user = Contact.query.get(user_id)
    if isinstance(user, Contact):
        return jsonify(user.serialize()), 200
    else:
        return jsonify({
            "result": "user not found"
        }), 404


########## Forma 2 de crear el Post con Validación de data#############################
@app.route('/contact', methods=['POST'])
def handle_contact():
    # First we get the payload json
    body = request.get_json()
    if isinstance(body, dict):
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'full_name' not in body:
            raise APIException('You need to specify the full_name', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
    
    else: return "no es un diccionario", 400        
    # at this point, all data has been validated, we can proceed to inster into the bd
    contact1 = Contact(email=body['email'], full_name =body['full_name'] )
    db.session.add(contact1)
    db.session.commit()
    return "ok", 200
######################################################################################

@app.route('/contact/<int:position>', methods=['DELETE'])
def delete_contact(position):
    contact_to_delete= Contact.query.get_or_404(position)
    db.session.delete(contact_to_delete)
    contact_to_delete.deleted = True 
    db.session.commit()
    return "borrado", 204

@app.route('/contact/<int:position>', methods=['GET'])
def handle_hello_users_for_id(position):
    contact = Contact.query.get(position)
    if contact is None:
        return "This contact doesn't exist", 404
    else:
        return jsonify(contact.serialize()),200


@app.route('/contact/<int:position>', methods=['PUT'])
def update_contact(position):
    # First we get the payload json
    body = request.get_json()
    if isinstance(body, dict):
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'full_name' not in body:
            raise APIException('You need to specify the full_name', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        
    else: return "no es un diccionario", 400        
    # at this point, all data has been validated, we can proceed to inster into the bd
    Contact.query.filter(Contact.id == position).update(({
        'email': body['email'],
        "full_name": body['full_name']
    })) 
    
    db.session.commit()
    return "ok", 200

@app.route('/contact/<int:position>', methods=['PATCH'])
def update_contact_property(position):
    body = request.get_json()
    contact_to_update = Contact.query.get(position)
    if contact_to_update is None:
        raise APIException("You need to specify the contact property", status_code=400)
    if 'full_name' != None:
        new_full_name = body['full_name']
        contact_to_update.full_name = new_full_name
    if 'email' != None:
        new_email = body['email']
        contact_to_update.email = new_email

    db.session.commit()
    return "Properties updated", 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=PORT, debug=False)
