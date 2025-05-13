from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
DB_NAME = "main.db"

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.getenv('USER_SERVICE_SECRET_KEY', 'default_user_secret')
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass # Already exists

    # Configure the database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, DB_NAME)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database
    db.init_app(app)

    # Import and register blueprints

    # Import models here to ensure they're registered with SQLAlchemy
    from .models import User, UserSession
    
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    # Create database tables
    with app.app_context():
        db.create_all()
        print(f"Database created at: {os.path.join(app.instance_path, DB_NAME)}")

    return app