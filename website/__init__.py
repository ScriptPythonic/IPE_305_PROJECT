from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
from os import path
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SECRET_KEY"] = "Oyemdade George"
    app.config['CLOUDINARY_URL'] = 'cloudinary://485855482193362:hvZOVNA9eJ8UVhJo5v-dODXHxAQ@dwxmvddcd'

    # Initialize Cloudinary
    cloudinary.config(
        cloud_name="dwxmvddcd",
        api_key="485855482193362",
        api_secret="hvZOVNA9eJ8UVhJo5v-dODXHxAQ"
    )

    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from .auth import auth
    from .views import views
    from .message import message

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(message, url_prefix='/')

    # Create database if it doesn't exist
    create_database(app)

    # Initialize Flask-Login
    login_manager.login_view = 'auth.login'  # Set the login view

    # Import User model for Flask-Login
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

def create_database(app):
    # Ensure the app context is active
    with app.app_context():
        # Create the database tables if they don't exist
        if not path.exists('website/' + DB_NAME):
            db.create_all()