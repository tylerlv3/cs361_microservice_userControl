from flask import Blueprint, request, jsonify
from .models import User, UserSession
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, timedelta

views = Blueprint('views', __name__)

@views.route('/check-user', methods=['POST'])
def check_user():
    """Checks if a user exists based on email."""
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({"error": "Email is required"}), 400

    email = data['email']
    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({"exists": True, "email": email}), 200
    else:
        return jsonify({"exists": False, "email": email}), 200 # Still 200 OK, just indicates not found


@views.route('/register', methods=['POST'])
def register():
    """Registers a new user."""
    print("Registering a new user")
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400

    email = data['email']
    password = data['password']
    name = data['name']

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    # Create new user
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(email=email, password_hash=hashed_password, name=name)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@views.route('/login', methods=['POST'])
def login():
    """Logs in a user."""
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Email and password are required"}), 400

    email = data['email']
    password = data['password']

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    session_token = secrets.token_hex(32)
    expires_at = datetime.now() + timedelta(days=30)
    # Create new session
    new_session = UserSession(
        token=session_token,
        user_id=user.id,
        expires_at=expires_at,
        is_active=True,
    )
    
    # Deactivate any existing sessions for this user
    UserSession.query.filter_by(user_id=user.id, is_active=True).update({'is_active': False})
    
    # Add and commit the new session
    db.session.add(new_session)
    db.session.commit()

    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "session_token": session_token,
        "email": user.email,
        "name": user.name
    }), 200

@views.route('/verify-session', methods=['POST'])
def verify_session():
    """Verify if a session token is valid."""
    data = request.get_json()
    if not data or 'session_token' not in data:
        return jsonify({"error": "Session token is required"}), 400

    session_token = data['session_token']
    session = UserSession.query.filter_by(
        token=session_token,
        is_active=True
    ).first()

    if not session:
        return jsonify({"error": "Invalid session"}), 401

    # Check if session has expired
    if datetime.utcnow() > session.expires_at:
        session.is_active = False
        db.session.commit()
        return jsonify({"error": "Session expired"}), 401

    return jsonify({
        "valid": True,
        "user_id": session.user_id,
        "email": session.user.email,
        "name": session.user.name
    }), 200


@views.route('/logout', methods=['POST'])
def logout():
    """Log out a user by invalidating their session."""
    data = request.get_json()
    if not data or 'session_token' not in data:
        return jsonify({"error": "Session token is required"}), 400

    session_token = data['session_token']
    session = UserSession.query.filter_by(token=session_token).first()
    
    if session:
        session.is_active = False
        db.session.commit()

    return jsonify({"message": "Logged out successfully"}), 200
    