"""
=========================================
CivicPulse Configuration
=========================================

Stores all application configuration
variables in one place.

Author : Sagar Sen
Project : CivicPulse
"""

import os

from dotenv import load_dotenv


load_dotenv()


class Config:

    # ==========================================
    # Flask Configuration
    # ==========================================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "default_secret_key"
    )

    DEBUG = True

    # ==========================================
    # Oracle Database Configuration
    # ==========================================

    ORACLE_USER = os.getenv("ORACLE_USER")

    ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")

    ORACLE_DSN = os.getenv("ORACLE_DSN")

    # ==========================================
    # Session Configuration
    # ==========================================

    SESSION_PERMANENT = False

    SESSION_TYPE = "filesystem"

    # ==========================================
    # Upload Configuration
    # ==========================================

    UPLOAD_FOLDER = "static/uploads"

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    ALLOWED_EXTENSIONS = {

        "png",

        "jpg",

        "jpeg"

    }

    # ==========================================
    # Password Security
    # ==========================================

    PASSWORD_MIN_LENGTH = 8