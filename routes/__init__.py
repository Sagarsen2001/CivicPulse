"""
=========================================
CivicPulse Routes Package
=========================================

This package contains all Flask
Blueprints used in the project.

Author : Sagar Sen
Project : CivicPulse
"""

from .public_routes import public_bp

from .api_routes import api_bp

from .auth_routes import auth_bp

from .citizen_routes import citizen_bp