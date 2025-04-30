from flask import Blueprint, request, jsonify
from .models import User
from . import db

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

# Add routes for registration and login later
# @views.route('/register', methods=['POST'])
# def register():
#     # ... implementation ...
#     pass

# @views.route('/login', methods=['POST'])
# def login():
#     # ... implementation ...
#     pass