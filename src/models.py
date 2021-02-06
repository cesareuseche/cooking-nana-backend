from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from base64 import b64encode
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import osimport json

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
    #bets_sent = db.relationship("Bet", backref="sender", foreign_keys="Bet.sender_id")
    #bets_received = db.relationship("Bet", backref="receiver", foreign_keys="Bet.receiver_id")

    #aca va el relationship con bet

    def __init__(self, email, name, last_name, ludos, username, password, status):
        self.email = email
        self.name = name
        self.last_name = last_name
        self.ludos = ludos
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
            100, 
            username, 
            password, 
            True
        )
        return new_contact


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
        sent_list = self.bets_sent
        received_list = self.bets_received
        bets_sent_serialize = list(map(lambda bet: bet.serialize(), sent_list))
        bets_received_serialize = list(map(lambda bet: bet.serialize(), received_list))
      
        return {
            'id' : self.id,
            'email' : self.email,
            'name' : self.name,
            'last_name' : self.last_name,
            'ludos' : self.ludos,
            'username' : self.username,
            'status' : self.status,
            #'bets_sent' : bets_sent_serialize,
            #'bets_received' : bets_received_serialize
        }

# class Bet(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     ludos = db.Column(db.Integer, nullable=False)
#     name = db.Column(db.String(50), nullable=False)
#     description = db.Column(db.String(120), nullable=False)
#     due_date = db.Column(db.DateTime(timezone=True), nullable=False)
#     create_date = db.Column(db.DateTime(timezone=True), nullable=False)
#     state = db.Column(db.String(11), nullable=False)
#     status = db.Column(db.Boolean, nullable=False)
#     winner_sender = db.Column(db.String(20))
#     winner_receiver = db.Column(db.String(20))
#     sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     receiver_id = db.Column(db.Integer, db.ForeignKey("user.id"))

#     def __init__(self, ludos, name, description, due_date, winner, state, status, winner_sender, winner_receiver, sender_id, receiver_id):
#             self.ludos = ludos
#             self.name = name
#             self.description = description
#             self.due_date = datetime.strptime(due_date, '%Y-%m-%dT%H:%M')
#             self.create_date = datetime.now(timezone.utc)
#             self.state = state
#             self.status = status
#             self.winner_sender = winner_sender
#             self.winner_receiver = winner_receiver
#             self.sender_id = sender_id
#             self.receiver_id = receiver_id
        
#     @classmethod
#     def create_bet(cls, ludos, name, description, due_date, sender_id, receiver_id):
#         new_bet = cls(
#             ludos, 
#             name.lower(), 
#             description.lower(), 
#             due_date,
#             "",
#             "enviado",
#             True,
#             "",
#             "",
#             sender_id,
#             receiver_id
#         )
#         return new_bet

#     def update_bet(self, dictionary):
#         for (key, value) in dictionary.items():
#             if hasattr(self, key):
#                 setattr(self, key, value)
#         return True

#     def check_date(self):
#         print(f"checking bet n {self.id}")
#         if (datetime.now() > self.due_date):
#             print(f"bet {self.id} is expired")
#             self.state = "expirado"
#             sender = User.query.get(self.sender_id)
#             sender.ludos += self.ludos
#             try: 
#                 db.session.commit()
#             except Exception as error:
#                 db.session.rollback()

#     def serializeBets(self):
#         return{
#             "id": self.id,
#             "name": self.name,
#             "state": self.state,
#             "status": self.status
#         }

#     def serialize(self):
#         sender = User.query.get(self.sender_id)
#         receiver = User.query.get(self.receiver_id)
#         return {
#             'id' : self.id,
#             'ludos' : self.ludos,
#             'name' : self.name,
#             'description' : self.description,
#             'due_date' : self.due_date,
#             'create_date' : self.create_date,
#             'state' : self.state,
#             'status' : self.status,
#             'winner_sender': self.winner_sender,
#             'winner_receiver': self.winner_receiver,
#             'sender_id' : self.sender_id,
#             'receiver_id' : self.receiver_id,
#             'sender': sender.username,
#             'receiver': receiver.username
#         }
    