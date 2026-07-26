"""
=========================================
CivicPulse Validation Service
=========================================

Performs validation for
registration and login forms.

Author : Sagar Sen
Project : CivicPulse
"""

import re


class ValidationService:

    @staticmethod
    def validate_registration(
        full_name,
        email,
        password,
        phone_number
    ):
        """
        Validate registration form.
        """

        # -----------------------------
        # Full Name
        # -----------------------------

        if not full_name or len(full_name.strip()) < 3:

            return False, "Full name must contain at least 3 characters."

        # -----------------------------
        # Email
        # -----------------------------

        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        if not re.match(email_pattern, email):

            return False, "Invalid email address."

        # -----------------------------
        # Password
        # -----------------------------

        if len(password) < 8:

            return False, "Password must be at least 8 characters long."

        # At least one uppercase letter

        if not re.search(r'[A-Z]', password):

            return False, "Password must contain at least one uppercase letter."

        # At least one lowercase letter

        if not re.search(r'[a-z]', password):

            return False, "Password must contain at least one lowercase letter."

        # At least one digit

        if not re.search(r'\d', password):

            return False, "Password must contain at least one number."

        # At least one special character

        if not re.search(r'[@$!%*?&#]', password):

            return False, "Password must contain at least one special character."

        # -----------------------------
        # Phone Number
        # -----------------------------

        phone_pattern = r'^[6-9]\d{9}$'

        if not re.match(phone_pattern, phone_number):

            return False, "Invalid phone number."

        return True, "Validation successful."

    @staticmethod
    def validate_login(
        email,
        password
    ):
        """
        Validate login form.
        """

        if not email:

            return False, "Email is required."

        if not password:

            return False, "Password is required."

        return True, "Validation successful."

    def validate_complaint(
        title,
        category,
        severity,
        location,
        description
    ):

        errors = []

        if len(title.strip()) < 5:
            errors.append("Title must contain at least 5 characters.")

        if category == "":
            errors.append("Please select a category.")

        if severity == "":
            errors.append("Please select severity.")

        if len(location.strip()) < 5:
            errors.append("Location is too short.")

        if len(description.strip()) < 20:
            errors.append("Description should contain at least 20 characters.")

        return errors