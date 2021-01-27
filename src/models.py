from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name= db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(10), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    phone = db.Column(db.String(40), unique=True, nullable=False)

    def __repr__(self):
        return '<Contact %r>' % self.full_name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "gender": self.gender,
            "is_active": self.is_active,
            "phone": self.phone,
            # do not serialize the password, its a security breach
        }

