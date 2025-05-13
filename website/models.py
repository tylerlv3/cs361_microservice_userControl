from . import db
from sqlalchemy.sql import func
from datetime import datetime, timedelta

# First define the User model
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # Define the relationship after Session class is defined
    sessions = db.relationship('UserSession', backref='user', lazy=True)

# Then define the Session model
class UserSession(db.Model):
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
    is_active = db.Column(db.Boolean, default=True)