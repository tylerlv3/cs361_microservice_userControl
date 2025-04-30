from . import db
# from flask_login import UserMixin # Keep for later login implementation
from sqlalchemy.sql import func

class User(db.Model): # Add UserMixin later if using Flask-Login
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150)) # Store hash, not plain password
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # Add other fields as needed: first_name, last_name, etc.