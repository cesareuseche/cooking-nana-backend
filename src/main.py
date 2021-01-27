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
from models import db, Contact
#from models import Person

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

############# forma 1 de declarar el método post pero sin validación de data#################
# @app.route('/contact', methods=['POST']) #debería recibir una lista de diccionarios
# def add_new_contact():
#     request_body = request.data
#     decoded_object = json.loads(request_body)
#     i=0
#     contact=[]
#     print("Incoming request with the following body", request_body)
#     if isinstance(decoded_object, list):
#         for i in decoded_object:
#             contact.append(i)
#             db.session.add(contact(i))
#             db.session.commit()
#     elif isinstance(decoded_object, dict):
#         contact.append(i)
#         db.session.add(contact)
#         db.session.commit()
#     else:
#         return "Error 400"
#     #return 'Response for the POST todo'
#     return jsonify(contact)
#####################################################################################

########## Forma 2 de crear el Post con Validación de data#############################
@app.route('/contact', methods=['POST'])
def add_new_contact():

    # First we get the payload json
    body = request.get_json()
    if isinstance(body, dict):
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'full_name' not in body:
            raise APIException('You need to specify the full_name', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'gender' not in body:
            raise APIException('You need to specify the gender', status_code=400)
        if 'is_active' not in body:
            raise APIException('You need to specify the is_active', status_code=400)
        if 'phone' not in body:
            raise APIException('You need to specify the phone', status_code=400)
    else:
        return "no se un diccionario", 400        
    # at this point, all data has been validated, we can proceed to inster into the bd
    contact1 = Contact(full_name=body['full_name'], email=body['email'], gender=['gender'], is_active=['is_active'], phone=['phone'])
    db.session.add(contact1)
    db.session.commit()
    return "ok", 200
######################################################################################

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
