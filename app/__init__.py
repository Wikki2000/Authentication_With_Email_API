#!/usr/bin/python3
""" Create the fask application. """
from flask import Flask
from os import getenv
from app.register import register_bp
from app.home import home_bp
from app.login import login_bp
from flask_jwt_extended import JWTManager

# Create an instance of JWTManager
jwt = JWTManager()

def create_app():
    """ create an instance of flask app. """
    app = Flask(__name__)
    app.secret_key = getenv("FLASK_SECRET_KEY")

    # Initialize JWTManager
    jwt.init_app(app)

    # Register the blueprint
    app.register_blueprint(register_bp, url_prefix="/api/auth")
    app.register_blueprint(home_bp, url_prefix="/api")
    app.register_blueprint(login_bp, url_prefix="/api/auth")

    return app
