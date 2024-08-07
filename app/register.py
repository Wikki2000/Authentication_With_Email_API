#!/usr/bin/python3
""" This module handles user registration. """
from flask import Blueprint, jsonify, request
from datetime import timedelta
from models.storage import Storage
from models.user import User
from secrets import randbelow
import sib_api_v3_sdk
from sqlalchemy.exc import IntegrityError
from os import getenv
from redis import Redis

# Register route blueprint
register_bp = Blueprint('register', __name__)

# Connect to redis database
r = Redis(host="localhost", port=6379, db=0)


@register_bp.route('/sent-confirmation-token', methods=['POST'])
def sent_confirmation_code():
    """ Sent token to mail for confirmation. """
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    # Check for empty request body
    if not data:
        error = {"status": "Bad Request",
                 "message": "Request body is empty"}
        return jsonify(error), 400

    # Check for required field
    required_field = ["name", "email"]
    for field in required_field:
        if not data.get(field):
            error = {"status": "Bad Request",
                     "message": f"{field} field require"}
            return jsonify(error), 400

    token = generate_token()

    # Sent token to recipient
    recipient = {"name": name, "email": email}
    response = send_token(token, "app/email_content.html", **recipient)
    if response:
        return jsonify({"status": "Success", "token": token,
                        "message": "Confirmation code sent to email"}), 200
    return jsonify({"status": "Error",
                    "message": "Token delivery failed"}), 500


@register_bp.route("/register", methods=['POST'])
def register():
    """ Store user credentials in database. """
    data = request.get_json()

    # Check for empty request body
    if not data:
        error = {"status": "Bad Request",
                 "message": "Request body is empty"}
        return jsonify(error), 400

    # Check for password
    required_field = ["first_name", "last_name", "email", "password", "token"]
    for field in required_field:
        if not data.get(field):
            error = {"status": "Bad Request",
                     "message": f"{field} field require"}
            return jsonify(error), 400

    # Check if token is valid
    token = data.get("token")
    retrieved_token = r.get(token)
    if not retrieved_token:
        error = {"status": "Validation Error",
                 "message": "Invalid or expired token"}
        return jsonify(error), 422

    # Create an instance of User class
    attribute = {"first_name": data.get("first_name"),
                 "last_name": data.get("last_name"),
                 "email": data.get("email"),
                 "password": data.get("password")}
    user = User(**attribute)
    try:
        if retrieved_token:
            user.hash_password()
            user.save()

            # Delete token after confirmation
            r.delete(token)

            return jsonify({"status": "Success",
                            "message": "Registration successfully",
                            "data": {
                                "id": user.id,
                                "first_name": user.first_name,
                                "last_name": user.last_name,
                                "email": user.email,
                                "password": user.password
                                }
                            }), 200
    except IntegrityError:
        session = Storage().get_session()
        error = {"status": "Validation Error",
                 "message": "Email is already registered"}
        session.rollback()
        return jsonify(error), 422
    finally:
        user.close()


def generate_token():
    """ Create a 6-digit token on every call. """
    token = str(randbelow(900000) + 100000)
    expiring_time = timedelta(minutes=15)

    # Save token to redis db and delete when expiring time ellapsed
    # The key of this token is the token itself
    r.setex(token, expiring_time, "valid")
    return token


def send_token(token, email_file, **recipient):
    """Send token to email.

    Args:
        token (string): The 6-digit email confirmation token.
        email_file (string): Path to email template file.
        kwargs (dict): Key-value pairs of recipient info.
    """
    config = sib_api_v3_sdk.Configuration()
    config.api_key["api-key"] = getenv("MAIL_API_KEY")

    # Create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(config)
    )

    sender = {"name": "Wikkisoft Company", "email": "wisdomokposin@gmail.com"}
    email_subject = "[AGS] Complete your registration"
    recipient = [recipient]

    recipient_name = recipient[0]["name"]
    email_content = read_email(email_file, token, recipient_name)

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=recipient,
            sender=sender,
            subject=email_subject,
            html_content=email_content
    )
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        return True
    except Exception:
        return False


def read_email(file_path, token, name):
    """Read email from file and substitue placeholder."""
    with open(file_path, "r") as file:
        content = file.read()
    content = content.replace("{{ name }}", name).replace("{{ token }}", token)
    return content
