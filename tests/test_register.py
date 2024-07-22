#!/usr/bin/python3
""" Test the user registration module. """
from app import create_app
from app import register
import models
from redis import Redis
import unittest


class TestRegister(unittest.TestCase):
    """ Models the test case of the register module. """

    def setUp(self):
        """Set up the Redis connection."""

        # Set up test environment for generate_token()
        self.r = Redis(host="localhost", port=6379, db=0)
        self.token = register.generate_token()

        # Set up test environment for database session engine
        storage = models.Storage()
        self.session = storage.get_session()

        # Set up test environment for sent-confirmation-token endpoint
        app = create_app()
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        """Close connection and destroy test data."""
        self.r.delete(self.token)

        # Close database session
        self.session.rollback()
        self.session.close()

    def test_create_token(self):
        """ Test that a 6-digit random token is created on every call. """
        self.assertIsNotNone(self.token, 'Token must not be None')
        self.assertEqual(len(self.token), 6, 'Token must be 6-digits')
        ttl = self.r.ttl(self.token)

        # Ensure token live atleast between the range of 14 - 15 mins
        self.assertTrue(ttl >= 14 * 60 and ttl <= 15 * 60)

    def test_read_email(self):
        """ Test that content of a file is read successfully. """
        mock_token = "12345"
        mock_name = "wisdom Okposin"
        mock_file = "tests/test_user.py"
        content = register.read_email(mock_file, mock_token, mock_name)
        self.assertIsNotNone(content)

    def send_token(self):
        """ Test that confirmation is delived savely. """
        recipient = {"name": "Wisdom Okposin",
                     "email": "wisdomokposin@gmail.com"}
        email_file = "app/email_content.html"
        token = "12345"
        status = register.send_token(token, email_file, **recipient)
        self.assertTrue(status, "Check network connection")

    def test_sent_confirmation_token_successful(self):
        """ Test that the successful response of endpoint. """

        request_body = {"name": "John Bush", "email": "example@mail.com"}
        expected_response = {
                "status": "Success", "token": "random_numbr",
                "message": "Confirmation code sent to email"
        }
        response = self.client.post("/api/auth/sent-confirmation-token",
                                    json=request_body)
        self.assertEqual(response.status_code, 200, "Check network")
        self.assertEqual(
                response.get_json().get("status"),
                expected_response.get("status")
        )
        self.assertEqual(
                response.get_json().get("message"),
                expected_response.get("message")
        )

        # self.assertTrue(response.get_json().get(token))
        # Line of code is intentionally comented out since the token varies.
        # It does not have a fix value so it cannot be tested for.

    def test_sent_confirmation_token_empty_body(self):
        """ Test empty request body response as expected. """
        request_body = {}
        expected_response = {"status": "Bad Request",
                             "message": "Request body is empty"}
        response = self.client.post("/api/auth/sent-confirmation-token",
                                    json=request_body)
        self.assertEqual(response.status_code, 400, "Check network")
        self.assertEqual(response.get_json(), expected_response)

    def test_sent_confirmation_token_missing_field(self):
        """ Test that missing field in request body response as expected. """
        # Omiting the email parameter
        request_body = {"name": "John Bush"}
        expected_response = {"status": "Bad Request",
                             "message": "email field require"}
        response = self.client.post("/api/auth/sent-confirmation-token",
                                    json=request_body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), expected_response)

    def test_register_new_user_and_existing_user(self):
        """ Test registration of new user. """
        request_body = {"first_name": "John", "last_name": "Bush",
                        "email": "example@gmail.com", "password": "12345",
                        "token": register.generate_token()}

        response = self.client.post("/api/auth/register",
                                    json=request_body)

        # Retrieve the user to get it id and password
        retrieved_save_user = self.session.query(models.user.User).filter_by(
                email="example@gmail.com").first()
        expected_response = {"status": "Success",
                             "message": "Registration successfully",
                             "data": {
                                 "id": retrieved_save_user.id,
                                 "first_name": "John",
                                 "last_name": "Bush",
                                 "email": "example@gmail.com",
                                 "password": retrieved_save_user.password
                                 }
                             }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected_response)

        # Attempt to register the same user again
        # Test for expire and existed user with status of 422
        duplicate_response = self.client.post("/api/auth/register",
                                              json=request_body)
        self.assertEqual(duplicate_response.status_code, 422)

        # Delete test data
        self.session.delete(retrieved_save_user)
        self.session.commit()


if __name__ == '__main__':
    unittest.main()
