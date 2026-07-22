"""
=========================================
CivicPulse Database Connection
=========================================

This module creates a reusable connection
to the Oracle Database.

Author : Sagar Sen
Project: CivicPulse
"""

import oracledb

from config import Config


def get_connection():
    """
    Create and return an Oracle database connection.
    """

    try:

        connection = oracledb.connect(

            user=Config.ORACLE_USER,

            password=Config.ORACLE_PASSWORD,

            dsn=Config.ORACLE_DSN

        )

        print("Oracle Database Connected Successfully.")

        return connection

    except oracledb.DatabaseError as error:

        print("Database Connection Error:")

        print(error)

        return None


def close_connection(connection):
    """
    Close the Oracle database connection.
    """

    if connection:

        connection.close()

        print("Oracle Database Connection Closed.")


# ==========================================
# Test Connection
# ==========================================

if __name__ == "__main__":

    conn = get_connection()

    if conn:

        close_connection(conn)