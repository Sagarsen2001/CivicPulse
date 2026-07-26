"""
=========================================
CivicPulse User Model
=========================================

Handles all database operations
related to users.

Author : Sagar Sen
Project : CivicPulse
"""

from database.connection import get_connection


class UserModel:

    @staticmethod
    def create_user(
        full_name,
        email,
        password,
        phone_number,
        role="Citizen"
    ):
        """
        Insert a new user into the USERS table.
        """

        connection = get_connection()

        if connection is None:
            return False

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO USERS
                (
                    FULL_NAME,
                    EMAIL,
                    USER_PASSWORD,
                    PHONE_NUMBER,
                    ROLE
                )
                VALUES
                (
                    :1,
                    :2,
                    :3,
                    :4,
                    :5
                )
                """,
                (
                    full_name,
                    email,
                    password,
                    phone_number,
                    role
                )
            )

            connection.commit()

            return True

        except Exception as error:

            print(error)

            connection.rollback()

            return False

        finally:

            cursor.close()
            connection.close()

    @staticmethod
    def get_user_by_email(email):
        """
        Find a user using email.
        """

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                USER_ID,
                FULL_NAME,
                EMAIL,
                USER_PASSWORD,
                PHONE_NUMBER,
                ROLE
            FROM USERS
            WHERE EMAIL = :1
            """,
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        return user

    @staticmethod
    def get_user_by_id(user_id):
        """
        Find a user using user ID.
        """

        connection = get_connection()

        if connection is None:
            return None

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                USER_ID,
                FULL_NAME,
                EMAIL,
                PHONE_NUMBER,
                ROLE
            FROM USERS
            WHERE USER_ID = :1
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        return user