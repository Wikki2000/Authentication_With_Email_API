#!/usr/python3
""" Test storage module """
from models.storage import Storage
import unittest
from models.user import User
from sqlalchemy.orm import Session


class TestStorage(unittest.TestCase):
    """ Define test cases for the database storage. """

    def setUp(self):
        """ Set up the test environment """
        self.user_data = {"first_name": "test_name",
                          "last_name": "test_last_name",
                          "email": "test@example.com",
                          "password": "test_password"
                          }

        self.user_obj = User(**self.user_data)
        self.storage_obj = Storage()
        self.session = self.storage_obj.get_session()

    def tearDown(self):
        """ Destroy data save during the each test """
        user = self.session.query(User).filter_by(
                email=self.user_data["email"]).first()

        if user:
            self.session.delete(user)
            self.session.commit()

    def test_get_session(self):
        """ Test that session engine was successfully created """
        self.assertIsInstance(self.session, Session)

    def test_get_engine(self):
        """ Test that the engine object is return correctly. """
        pass

    def test_add(self):
        """ Test that a user object is added to new session. """
        self.storage_obj.add(self.user_obj)
        self.assertIn(self.user_obj, self.session.new)

    def test_save(self):
        """ Test if the save changes persist in the database. """
        self.session.add(self.user_obj)
        self.storage_obj.save()
        self.assertNotIn(self.user_obj, self.session.new)

        # Check if correct data is save to db
        user = self.session.query(User).filter_by(
                email=self.user_data["email"]).first()
        self.assertEqual(self.user_data["last_name"], user.last_name)
        self.assertEqual(self.user_data["first_name"], user.first_name)
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.create_at)

    def test_get_by_email(self):
        """ Test if user is correctly retrieved by it email. """
        self.session.add(self.user_obj)
        self.session.commit()

        # Retrieving a user that exists
        retrieved_user = self.storage_obj.get_by_email(
                User, self.user_data["email"]
        )
        self.assertIsInstance(retrieved_user, User)

        # Retrieving non-existence user
        retrieved_user = self.storage_obj.get_by_email(User, "wrong@mail.com")
        self.assertIsNone(retrieved_user)

    def test_close(self):
        """ Test if session is successfully close. """
        self.storage_obj.close()
        self.assertIsNotNone(self.session)


if __name__ == '__main__':
    unittest.main()
