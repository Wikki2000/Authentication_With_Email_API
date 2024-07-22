#!/usr/bin/python3
"""This module models the storage of user details"""
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()


class User(Base):
    """ Define the class models for user """
    __tablename__ = "users"
    id = Column(String(50), primary_key=True,
                nullable=False, default=lambda: str(uuid4()))
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(1500), nullable=False)
    create_at = Column(DateTime, nullable=False, default=datetime.now())

    def hash_password(self):
        """ Hash password before storing in database. """
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        """ Verify password and give access. """
        return check_password_hash(self.password, password)

    def save(self):
        """ Save a user instance to a database. """
        models.storage.add(self)
        models.storage.save()

    def get_session(self):
        """ Get session engine to connect database. """
        session = models.storage.get_session()
        return session

    def delete(self):
        """ Delete an instance of user class. """
        models.storage.delete(self)
        models.storage.save()

    def close(self):
        """ Close database session. """
        models.storage.close()
