from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
DB_NAME = "users.db"

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.getenv('USER_SERVICE_SECRET_KEY', 'default_user_secret') # Use a specific key for this service
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass # Already exists

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.instance_path, DB_NAME)}'
    db.init_app(app)

    from .views import views
    from .models import User # Import models here

    app.register_blueprint(views, url_prefix='/')

    with app.app_context():
        db.create_all() # Create tables

    return app