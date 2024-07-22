#!/usr/bin/python3
"""Define the home view of API."""
from flask import Blueprint, jsonify

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    """Define the home view of the application."""
    return jsonify({"status": "Success",
                    "message": "Connection Secure"})
