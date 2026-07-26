"""
=========================================
CivicPulse Authentication Service
=========================================

Handles user registration,
login, and password security.

Author : Sagar Sen
Project : CivicPulse
"""

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models.user_model import UserModel
from services.validation_service import ValidationService


class AuthService:

    @staticmethod
    def register_user(
        full_name,
        email,
        password,
        phone_number
    ):
        """
        Register a new user.
        """

        valid, message = ValidationService.validate_registration(

            full_name,
            email,
            password,
            phone_number

        )

        if not valid:

            return False, message

        existing_user = UserModel.get_user_by_email(email)

        if existing_user:

            return False, "Email already exists."

        hashed_password = generate_password_hash(password)

        success = UserModel.create_user(

            full_name=full_name,

            email=email,

            password=hashed_password,

            phone_number=phone_number

        )

        if success:

            return True, "Registration successful."

        return False, "Registration failed."


    @staticmethod
    def login_user(
        email,
        password
    ):
        """
        Authenticate a user.
        """

        user = UserModel.get_user_by_email(email)

        if user is None:

            return False, None, "Invalid email or password."

        stored_password = user[3]

        if not check_password_hash(

            stored_password,

            password

        ):

            return False, None, "Invalid email or password."

        return True, user, "Login successful."