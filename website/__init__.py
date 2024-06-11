from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os import path
db = SQLAlchemy()
DB_NAME = "database.db"

def Create_app():
  app = Flask(__name__)
  app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
  app.config["SECRET_KEY"]= "Oyemdade George"
  
  from .auth import auth
  from .views import views 
  
  app.register_blueprint(auth,url_prefix='/')
  app.register_blueprint(views,url_prefix='/')
  
  db.init_app(app)
  create_database(app)
  return app
 
def create_database(app):
   with app.app_context():
       if not path.exists('website/' + DB_NAME):
           db.create_all()