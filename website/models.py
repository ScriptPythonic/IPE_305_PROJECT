from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matric_no = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(255), default='https://th.bing.com/th/id/R.d8be3ebdc1ed3c6b13ffbeee0b20fa3c?rik=h%2bwbaNZzYT67Gg&pid=ImgRaw&r=0')
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.full_name}>'
    
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    file_url = db.Column(db.String(300), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

