"""
=========================================
CivicPulse End-to-End Test Suite
=========================================

Comprehensive test suite covering:
- Flask App & Blueprint Registration
- Security Headers (Day 26)
- Public Pages (Home, About, How it works, Categories)
- Authentication & Validation
- Role-Based Access Control (RBAC) (Citizen, Admin, Worker)
- Citizen Grievance Submission & Details
- Admin Dashboard, Complaints Review, CSV Export
- Worker Dashboard & Assignment Integrity
- Duplicate Detection Algorithms (Day 21)
- Email Notification Graceful Fallbacks (Day 20)
- File Upload Validation (Day 10, 18)

Author : Sagar Sen
Project : CivicPulse
"""

import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app
from utils.file_utils import allowed_file, generate_unique_filename, get_file_extension
from services.duplicate_service import DuplicateDetectionService
from services.notification_service import NotificationService
from services.validation_service import ValidationService


@pytest.fixture
def client():
    """Create Flask test client with testing mode enabled."""
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


# ==========================================
# 1. Application & Security Headers Tests
# ==========================================

def test_app_initialization(client):
    """Test that app starts and all blueprints are registered."""
    assert app is not None
    rules = [r.rule for r in app.url_map.iter_rules()]
    assert "/" in rules
    assert "/auth/login" in rules
    assert "/citizen/dashboard" in rules
    assert "/admin/dashboard" in rules
    assert "/worker/dashboard" in rules
    assert "/api/categories" in rules


def test_security_headers(client):
    """Day 26: Test that security headers are applied to HTTP responses."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "SAMEORIGIN"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"


# ==========================================
# 2. Public Routes Tests
# ==========================================

def test_public_pages(client):
    """Test that all public static information pages load with HTTP 200."""
    pages = ["/", "/about", "/how-it-works", "/categories"]
    for page in pages:
        res = client.get(page)
        assert res.status_code == 200, f"Page {page} failed to load"
        assert b"CivicPulse" in res.data


def test_api_categories(client):
    """Test API endpoint returning category list."""
    res = client.get("/api/categories")
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data["success"] is True
    assert len(json_data["categories"]) > 0


# ==========================================
# 3. Role-Based Access Control (RBAC) Tests
# ==========================================

def test_unauthenticated_protected_routes(client):
    """Test that unauthenticated requests to protected dashboards redirect to login."""
    protected = ["/citizen/dashboard", "/admin/dashboard", "/worker/dashboard"]
    for route in protected:
        res = client.get(route, follow_redirects=False)
        assert res.status_code == 302
        assert "/auth/login" in res.headers["Location"]


def test_citizen_cannot_access_admin_dashboard(client):
    """Test that authenticated citizen cannot access admin dashboard."""
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["user_name"] = "Test Citizen"
        sess["user_role"] = "Citizen"

    res = client.get("/admin/dashboard", follow_redirects=False)
    assert res.status_code == 302
    assert "/auth/unauthorized" in res.headers["Location"]


def test_worker_cannot_access_admin_dashboard(client):
    """Test that authenticated worker cannot access admin dashboard."""
    with client.session_transaction() as sess:
        sess["user_id"] = 100
        sess["user_name"] = "Test Worker"
        sess["user_role"] = "Worker"

    res = client.get("/admin/dashboard", follow_redirects=False)
    assert res.status_code == 302
    assert "/auth/unauthorized" in res.headers["Location"]


# ==========================================
# 4. Admin Feature Tests (Days 13-15, 24, 25)
# ==========================================

def test_admin_authorized_access(client):
    """Test that an admin can access all admin views."""
    with client.session_transaction() as sess:
        sess["user_id"] = 3
        sess["user_name"] = "Admin User"
        sess["user_role"] = "Admin"

    # Dashboard (Day 13)
    res = client.get("/admin/dashboard")
    assert res.status_code == 200
    assert b"Admin Dashboard" in res.data

    # Complaints Management (Day 14)
    res = client.get("/admin/complaints")
    assert res.status_code == 200
    assert b"Complaints Management" in res.data

    # Workers Directory (Day 15)
    res = client.get("/admin/workers")
    assert res.status_code == 200
    assert b"Municipal Field Workers" in res.data

    # Map View (Day 24)
    res = client.get("/admin/map")
    assert res.status_code == 200
    assert b"Geographic Complaint Map" in res.data

    # Analytics Dashboard (Day 25)
    res = client.get("/admin/analytics")
    assert res.status_code == 200
    assert b"Municipal Analytics" in res.data

    # CSV Export (Day 25)
    res = client.get("/admin/export-csv")
    assert res.status_code == 200
    assert res.mimetype == "text/csv"
    assert b"Complaint ID,Title,Category" in res.data


# ==========================================
# 5. Worker Feature Tests (Days 16, 17, 18)
# ==========================================

def test_worker_authorized_dashboard(client):
    """Test that an authorized field worker can access their task dashboard."""
    with client.session_transaction() as sess:
        sess["user_id"] = 100
        sess["user_name"] = "Rajesh Kumar"
        sess["user_role"] = "Worker"

    res = client.get("/worker/dashboard")
    assert res.status_code == 200
    assert b"Field Worker Dashboard" in res.data


# ==========================================
# 6. Citizen Dashboard & Workflow (Days 8-12, 19, 22)
# ==========================================

def test_citizen_authorized_dashboard(client):
    """Test that an authorized citizen can access their dashboard."""
    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["user_name"] = "Rahul Sharma"
        sess["user_role"] = "Citizen"

    res = client.get("/citizen/dashboard")
    assert res.status_code == 200
    assert b"Welcome, Rahul Sharma" in res.data

    res = client.get("/citizen/my-complaints")
    assert res.status_code == 200
    assert b"My Complaints" in res.data


# ==========================================
# 7. Form Validation Tests
# ==========================================

def test_registration_validation():
    """Test password and email validation rules."""
    # Short password
    valid, msg = ValidationService.validate_registration("Rahul", "rahul@test.com", "weak", "9876543210")
    assert not valid
    assert "8 characters" in msg

    # Missing uppercase
    valid, msg = ValidationService.validate_registration("Rahul", "rahul@test.com", "lowercase1!", "9876543210")
    assert not valid
    assert "uppercase" in msg

    # Invalid phone
    valid, msg = ValidationService.validate_registration("Rahul", "rahul@test.com", "ValidPass1!", "12345")
    assert not valid
    assert "phone" in msg.lower()

    # Valid registration
    valid, msg = ValidationService.validate_registration("Rahul Sharma", "rahul@test.com", "ValidPass1!", "9876543210")
    assert valid


def test_complaint_validation():
    """Test complaint submission validation rules."""
    errors = ValidationService.validate_complaint("poth", "", "", "loc", "short")
    assert len(errors) > 0
    assert any("Title" in e for e in errors)
    assert any("category" in e.lower() for e in errors)
    assert any("severity" in e.lower() for e in errors)


# ==========================================
# 8. Duplicate Detection Service (Day 21)
# ==========================================

def test_haversine_distance():
    """Test mathematical distance calculation between GPS coordinates."""
    # Same point
    d = DuplicateDetectionService.haversine_distance(17.9784, 79.5941, 17.9784, 79.5941)
    assert d == 0.0

    # Approx 50 meters away
    d50m = DuplicateDetectionService.haversine_distance(17.9784, 79.5941, 17.9788, 79.5941)
    assert 30 < d50m < 60

    # None coordinate handling
    assert DuplicateDetectionService.haversine_distance(None, 79.5941, 17.9784, 79.5941) is None


def test_duplicate_text_similarity():
    """Test fallback text similarity calculation."""
    sim = DuplicateDetectionService._basic_text_similarity("Deep pothole on main road", "A deep pothole on the main road")
    assert sim > 0.6

    sim_diff = DuplicateDetectionService._basic_text_similarity("Deep pothole on main road", "Street light broken in market")
    assert sim_diff < 0.2


# ==========================================
# 9. Notification Service Tests (Day 20)
# ==========================================

def test_notification_graceful_fallback():
    """Day 20: Test that notification service does not crash when SMTP is unconfigured."""
    success, msg = NotificationService.notify_complaint_submitted("user@example.com", "Test User", 999, "Test Issue")
    # Should report disabled / skipped gracefully without throwing exception
    assert success is False
    assert "SMTP not configured" in msg or "Email delivery is disabled" in msg


# ==========================================
# 10. File Utils & Upload Security Tests (Day 10, 18, 26)
# ==========================================

def test_file_utils():
    """Test safe file extension check and unique filename generation."""
    # Allowed
    assert allowed_file("pothole.png") is True
    assert allowed_file("proof.jpg") is True
    assert allowed_file("evidence.jpeg") is True
    assert allowed_file("damage.webp") is True

    # Blocked dangerous extensions
    assert allowed_file("exploit.php") is False
    assert allowed_file("virus.exe") is False
    assert allowed_file("script.sh") is False
    assert allowed_file("backdoor.py") is False
    assert allowed_file("noextension") is False
    assert allowed_file("") is False

    # Unique filename generation
    name1 = generate_unique_filename("test.jpg")
    name2 = generate_unique_filename("test.jpg")
    assert name1 != name2
    assert name1.endswith(".jpg")
    assert len(name1) > 32
