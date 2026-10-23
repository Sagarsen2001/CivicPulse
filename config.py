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
        "civicpulse-secret-key-change-in-production-2026"
    )

    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")

    # ==========================================
    # Security & Cookie Settings (Day 26)
    # ==========================================

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    # ==========================================
    # Oracle Database Configuration
    # ==========================================

    ORACLE_USER = os.getenv("ORACLE_USER", "system")
    ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "")
    ORACLE_DSN = os.getenv("ORACLE_DSN", "localhost:1521/FREEPDB1")

    # ==========================================
    # Upload Configuration
    # ==========================================

    UPLOAD_FOLDER = os.path.join("static", "uploads")
    COMPLAINT_IMAGE_FOLDER = os.path.join("static", "uploads", "complaint_images")
    RESOLUTION_PROOF_FOLDER = os.path.join("static", "uploads", "resolution_proofs")

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max upload

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "webp"
    }

    # ==========================================
    # SMTP Email Configuration (Day 20)
    # ==========================================

    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "noreply@civicpulse.com")
    SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "CivicPulse")

    # ==========================================
    # Password Security
    # ==========================================

    PASSWORD_MIN_LENGTH = 8