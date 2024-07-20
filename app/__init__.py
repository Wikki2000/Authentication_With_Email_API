#!/usr/bin/python3
""" Create the fask application. """
from flask import Flask
from os import getenv
from app.register import register_bp


def create_app():
    """ create an instance of flask app. """
    app = Flask(__name__)
    app.register_blueprint(register_bp, url_prefix="/api/auth")
    app.secret_key = getenv("FLASK_SECRET_KEY")
    return app
