#!/usr/python3
"""Models test case for login routes."""
from app import create_app
import unittest
from models.user import User
from models.storage import Storage


class TestLogin(unittest.TestCase):
    """Define test case for login routes."""

    def setUp(self):
        """Set up test environment for login routes."""
        self.user_data = {"first_name": "John", "last_name": "Bush",
                          "email": "example@mail.com", "password": "12345"}
        self.user_obj = User(**self.user_data)
        self.user_obj.hash_password()
        self.storage = Storage()
        self.session = self.storage.get_session()

        app = create_app()
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        """Destroy test data after completion."""
        user = self.session.query(User).filter_by(
                email=self.user_data["email"]).first()
        if user:
            self.session.delete(user)
            self.session.commit()

    def test_login_successful(self):
        """Test login with valid credentials."""
        # Register user in database
        self.session.add(self.user_obj)
        self.session.commit()

        request_body = {"email": "example@mail.com", "password": "12345"}
        response = self.client.post("/api/auth/login",
                                    json=request_body)
        response_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get("status"), "success")
        self.assertEqual(response_data.get("message"), "Login successful")
        self.assertIsNotNone(response_data.get("data"))

    def test_login_with_empty_request_body(self):
        """Test request with empty body"""
        request_body = {}
        expected_response = {"status": "Bad Request",
                             "message": "Empty request body"}
        response = self.client.post("/api/auth/login",
                                    json=request_body)
        response_data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_response, response_data)

    def test_login_with_missing_field(self):
        """Test authentication with missing parameters."""
        # Password missing among the parameter
        request_body = {"email": "example@mail.com"}
        expected_response = {"status": "Bad Request",
                             "message": "password field require"}
        response = self.client.post("/api/auth/login",
                                    json=request_body)
        response_data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_response, response_data)

    def test_login_with_invalid_credentials(self):
        """Test authentication with invalid credentials"""
        request_body = {"email": "wrong_email", "password": "wrong_pwd"}
        expected_response = {"status": "Unauthorized Access",
                             "message": "Invalid email or password"}
        response = self.client.post("/api/auth/login",
                                    json=request_body)
        response_data = response.get_json()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(expected_response, response_data)


if __name__ == "__main__":
    unittest.main()
