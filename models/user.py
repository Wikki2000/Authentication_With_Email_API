#!/usr/bin/python3
"""This module models the storage of user details"""
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from uuid import uuid4

Base = declarative_base()


class User(Base):
    """ Define the class models for user """
    __tablename__ = "users"
    id = Column(String(50), primary_key=True,
                nullable=False, default=lambda: str(uuid4()))
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    create_at = Column(DateTime, nullable=False, default=datetime.now())

    @classmethod
    def get_by_email(cls, email):
        """ Retrieve user by email. """
        user = models.storage.get_by_email(cls, email)
        return user

    def save(self):
        """ Save a user instance to a database. """
        models.storage.add(self)
        models.storage.save()

    def close(self):
        """ Close database session. """
        models.storage.close()
