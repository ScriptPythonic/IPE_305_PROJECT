from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matric_no = db.Column(db.String(100), unique=True)
    full_name = db.Column(db.String(100))
    phone_number = db.Column(db.Integer)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
