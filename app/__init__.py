from flask import Flask
from app.models import db
from config import config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os


def create_app(config_name='development'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])

    app.secret_key = 'SOME KEY'

    login_manager = LoginManager()
    login_manager.init_app(app)

    from app.models import User
    
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(int(uid))
    
    bcrypt = Bcrypt(app)
    
    # Initialize database
    db.init_app(app)

    
    # Register blueprints
    from app.routes import register_routes
    register_routes(app, db, bcrypt)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

