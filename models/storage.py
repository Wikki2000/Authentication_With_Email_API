#!/usr/bin/python3
"""This module models the storage of the authentication API"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv


class Storage:
    """ Defines storage model using SQLAlchemy. """
    __session = None
    __engine = None

    def __init__(self):
        from models.user import Base
        """ Create session engine to interact with database. """
        username = getenv('USER_NAME')
        password = getenv('PASSWORD')
        database = getenv('DATABASE')

        if not username or not password:
            error = "Environment variables must be set for database URL"
            raise ValueError(error)

        url = f'postgresql://{username}:{password}@localhost:5432/{database}'
        self.__engine = create_engine(url, pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine)
        self.__session = session()

    def get_session(self):
        """ Get the session engine for connecting to the database. """
        return self.__session

    def get_engine(self):
        """ Get the engine object """
        return self.__engine

    def get_by_email(self, cls, email):
        """ Retrieve user by email. """
        user = self.__session.query(cls).filter_by(email=email).first()

        # Check if user found
        if not user:
            return None
        return user

    def add(self, obj):
        """ Add user object to session.new """
        self.__session.add(obj)

    def save(self):
        """ Commit change to database """
        self.__session.commit()

    def close(self):
        """ Close database session. """
        self.__session.close()
