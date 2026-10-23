"""
=========================================
CivicPulse API Routes
=========================================

Endpoints for AJAX and interactive features:
- Categories List
- Duplicate Complaint Detection (Day 21)
- Geo-location / Map Markers (Day 24)

Author : Sagar Sen
Project: CivicPulse
"""

from flask import Blueprint, jsonify, request
from database.connection import get_connection
from services.duplicate_service import DuplicateDetectionService
from models.complaint_model import ComplaintModel

api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


# ==========================================
# Categories API
# ==========================================

@api_bp.route("/categories", methods=["GET"])
def get_categories():
    connection = get_connection()
    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT
                CATEGORY_ID,
                CATEGORY_NAME,
                DESCRIPTION
            FROM ISSUE_CATEGORIES
            ORDER BY CATEGORY_NAME
        """)

        categories = []
        for row in cursor.fetchall():
            categories.append({
                "category_id": row[0],
                "category_name": row[1],
                "description": row[2]
            })

        return jsonify({
            "success": True,
            "categories": categories
        })
    finally:
        cursor.close()
        connection.close()


# ==========================================
# Day 21: Duplicate Complaint Detection API
# ==========================================

@api_bp.route("/check-duplicates", methods=["POST"])
def check_duplicates():
    """
    Checks for potential duplicate complaints based on title,
    description, category, and GPS proximity.
    """
    data = request.get_json(silent=True) or request.form

    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    category = data.get("category_id") or data.get("category")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if not title and not description:
        return jsonify({"success": True, "duplicates": []})

    try:
        category_id = int(category) if category else None
    except (ValueError, TypeError):
        category_id = None

    if not category_id:
        return jsonify({"success": True, "duplicates": []})

    lat_val = None
    lng_val = None
    if latitude and longitude:
        try:
            lat_val = float(latitude)
            lng_val = float(longitude)
        except ValueError:
            pass

    duplicates = DuplicateDetectionService.find_duplicates(
        title=title,
        description=description,
        category_id=category_id,
        latitude=lat_val,
        longitude=lng_val
    )

    return jsonify({
        "success": True,
        "count": len(duplicates),
        "duplicates": duplicates
    })


# ==========================================
# Day 24: Map Markers API
# ==========================================

@api_bp.route("/map-markers", methods=["GET"])
def get_map_markers():
    """Returns geo-tagged complaints for map visualizations."""
    markers = ComplaintModel.get_map_markers()
    return jsonify({
        "success": True,
        "count": len(markers),
        "markers": markers
    })