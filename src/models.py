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
    #bets_sent = db.relationship("Bet", backref="sender", foreign_keys="Bet.sender_id")
    #bets_received = db.relationship("Bet", backref="receiver", foreign_keys="Bet.receiver_id")

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
            'username' : self.username,
            'status' : self.status,
        }
