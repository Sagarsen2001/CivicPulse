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

    # ==========================================
    # Oracle Database Configuration
    # ==========================================

    ORACLE_USER = os.getenv("ORACLE_USER")

    ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")

    ORACLE_DSN = os.getenv("ORACLE_DSN")