"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Contact#, Recipe, Ingredient


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
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

@app.route('/contact', methods=['GET'])
def handle_hello_users():
    contacts = Contact.query.all()
    response_body = []
    for contact in contacts:
        response_body.append(contact.serialize())

    return jsonify(response_body), 200    

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
