#!/usr/python3
""" Test the user module """
from models.user import User
from models.storage import Storage
import unittest 


class TestUser(unittest.TestCase):
    """ Models test cases for User class. """
    
    def setUp(self):
        """ Set up the test environment. """
        self.user_data = {"first_name": "test_name",
                          "last_name": "test_last_name",
                          "email": "test@example.com",
                          "password": "test_password"
                          }
        self.obj = User(**self.user_data)

        # Get session object
        storage = Storage()
        self.session = storage.get_session()

    def tearDown(self):
        """ Destroy the test data each time the test is ran."""
        user = self.session.query(User).filter_by(
                email=self.user_data["email"]).first()
        if user:
            self.session.delete(user)
            self.session.commit()

    def test_initialization(self):
        """ Test the initialization of class. """
        self.assertIsInstance(self.obj, User)

    def test_save(self):
        """ Ensure that user instance is save """
        self.obj.save()

        # Retrieve the save user and check if it's an instance of User
        user = self.session.query(User).filter_by(
                email=self.user_data["email"]).first()
        self.assertIsInstance(user, User)

    def test_close(self):
        """ Test that session is close successfully."""
        self.obj.close()
        self.assertIsNone(self.session)

if __name__ == "__main__":
    unittest.main()
