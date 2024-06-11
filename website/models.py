from . import db
from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matric_no = db.Column(db.String(100), unique=True)
    full_name = db.Column(db.String(100))
    phone_number = db.Column(db.Integer)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
