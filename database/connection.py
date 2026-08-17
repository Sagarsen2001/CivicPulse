"""
=========================================
CivicPulse Database Connection
=========================================

Creates a reusable Oracle database connection.

Author : Sagar Sen
Project: CivicPulse
"""

import oracledb

from config import Config


# ==========================================
# Create Oracle Connection
# ==========================================

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

        print("✅ Oracle Database Connected Successfully.")

        return connection

    except oracledb.DatabaseError as error:

        print("❌ Database Connection Error:")
        print(error)

        return None


# ==========================================
# Close Oracle Connection
# ==========================================

def close_connection(connection):
    """
    Close the Oracle database connection.
    """

    if connection:

        try:

            connection.close()

            print("✅ Oracle Database Connection Closed.")

        except oracledb.DatabaseError as error:

            print("❌ Error Closing Database Connection:")
            print(error)


# ==========================================
# Test Connection
# ==========================================

if __name__ == "__main__":

    print("Testing Oracle Connection...\n")

    print(
        "Oracle User :",
        Config.ORACLE_USER
    )

    print(
        "Oracle DSN  :",
        Config.ORACLE_DSN
    )

    connection = get_connection()

    if connection:

        close_connection(connection)