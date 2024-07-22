#!/usr/bin/python3
"""Models user login route."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from models.storage import Storage


# Initialize amd create database map table
db = Storage()

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["POST"])
def login():
    """Defines the login routes of user."""
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "Bad Request",
            "message": "Empty request body"
        }), 400

    required_field = ["email", "password"]
    for field in required_field:
        if not data.get(field):
            return jsonify({
                "status": "Bad Request",
                "message": f"{field} field require"
            }), 400

    email = data.get("email")
    password = data.get("password")

    session = db.get_session()

    user = session.query(User).filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "data": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "access_token": access_token
            }
        }), 200

    # Return for invalid credentials
    return jsonify({"status": "Unauthorized Access",
                    "message": "Invalid email or password"}), 401
