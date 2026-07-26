"""
=========================================
CivicPulse Constants
=========================================

Stores all constants used throughout
the application.

Author : Sagar Sen
Project : CivicPulse
"""

# ==========================================
# User Roles
# ==========================================

CITIZEN = "Citizen"

ADMIN = "Admin"

WORKER = "Worker"


ROLES = [

    CITIZEN,

    ADMIN,

    WORKER

]


# ==========================================
# Complaint Status
# ==========================================

PENDING = "Pending"

VERIFIED = "Verified"

ASSIGNED = "Assigned"

IN_PROGRESS = "In Progress"

RESOLVED = "Resolved"

REJECTED = "Rejected"


COMPLAINT_STATUS = [

    PENDING,

    VERIFIED,

    ASSIGNED,

    IN_PROGRESS,

    RESOLVED,

    REJECTED

]


# ==========================================
# Complaint Categories
# ==========================================

GARBAGE = "Garbage"

POTHOLE = "Pothole"

DRAINAGE = "Drainage"

STREET_LIGHT = "Street Light"

WATER_LEAKAGE = "Water Leakage"

TRAFFIC_SIGNAL = "Traffic Signal"


COMPLAINT_CATEGORIES = [

    GARBAGE,

    POTHOLE,

    DRAINAGE,

    STREET_LIGHT,

    WATER_LEAKAGE,

    TRAFFIC_SIGNAL

]


# ==========================================
# Severity Levels
# ==========================================

LOW = "Low"

MEDIUM = "Medium"

HIGH = "High"

CRITICAL = "Critical"


SEVERITY_LEVELS = [

    LOW,

    MEDIUM,

    HIGH,

    CRITICAL

]