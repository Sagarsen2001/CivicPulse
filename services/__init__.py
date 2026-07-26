"""
=========================================
CivicPulse Services Package
=========================================

This package contains all business logic
used in the CivicPulse project.

Current Services
----------------
- auth_service
- validation_service

Future Services
---------------
- complaint_service
- image_service
- status_service
- assignment_service
- feedback_service
- priority_service
- duplicate_service
- analytics_service
- escalation_service

Author : Sagar Sen
Project : CivicPulse
"""

from .auth_service import AuthService
from .validation_service import ValidationService