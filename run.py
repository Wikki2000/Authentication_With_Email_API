#!/usr/bin/python3
"""
Main entry point for the application.

This script initializes and starts the Flask web application.
It imports the necessary modules, creates the app instance,
initializes the database, and runs the app.
"""
from app import create_app
from models.storage import Storage

app = create_app()

# Initialize database and create associated tables
Storage()

if __name__ == "__main__":
    app.run(debug=True)
