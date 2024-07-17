#!/usr/python3
""" Test the user module """
from models.user import User
from models.storage import Storage
import unittest 

storage = Storage()
session = storage.get_session()

user_data = {"first_name": "test_name",
             "last_name": "test_last_name",
             "email": "test@example.com",
             "password": "test_password"
             }
obj = User(**user_data)

session.add(obj)
session.flush()

print(obj.id)
print(obj.create_at)
print(obj.email)
