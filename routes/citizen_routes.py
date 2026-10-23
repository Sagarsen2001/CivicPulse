"""
=========================================
CivicPulse Citizen Routes
=========================================

Handles all citizen-related pages:
- Citizen Dashboard (Day 8)
- Report Issue with Image Upload & Coordinates (Day 9, 10, 24)
- My Complaints with Search & Filter (Day 11)
- Complaint Details & Progress Tracking (Day 12, 19)
- Upvoting Complaints (Day 22)
- Resolution Feedback (Day 22)

Author : Sagar Sen
Project: CivicPulse
"""

import os
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session,
    current_app,
    jsonify
)

from utils.decorators import login_required, citizen_required
from utils.file_utils import allowed_file, generate_unique_filename
from services.validation_service import ValidationService
from services.complaint_service import ComplaintService
from services.notification_service import NotificationService
from models.complaint_model import ComplaintModel
from models.status_history_model import StatusHistoryModel
from models.complaint_image_model import ComplaintImageModel


citizen_bp = Blueprint(
    "citizen",
    __name__,
    url_prefix="/citizen"
)


# ==========================================
# Citizen Dashboard
# ==========================================

@citizen_bp.route("/dashboard")
@login_required
@citizen_required
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please login again.", "warning")
        return redirect(url_for("auth.login"))

    dashboard_data = ComplaintService.get_dashboard_data(user_id)
    return render_template(
        "citizen/dashboard.html",
        **dashboard_data
    )


# ==========================================
# Report Issue
# ==========================================

@citizen_bp.route("/report-issue", methods=["GET", "POST"])
@login_required
@citizen_required
def report_issue():
    if request.method == "POST":
        user_id = session.get("user_id")
        user_email = session.get("user_email")
        user_name = session.get("user_name", "Citizen")

        if not user_id:
            flash("User session not found. Please login again.", "danger")
            return redirect(url_for("auth.login"))

        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        severity = request.form.get("severity", "").strip()
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        image = request.files.get("image")

        # Validation
        errors = ValidationService.validate_complaint(
            title, category, severity, location, description
        )

        if errors:
            for error in errors:
                flash(error, "danger")
            return redirect(url_for("citizen.report_issue"))

        try:
            category_id = int(category)
        except (TypeError, ValueError):
            flash("Invalid complaint category.", "danger")
            return redirect(url_for("citizen.report_issue"))

        # Parse coordinates safely
        lat_val = None
        lng_val = None
        if latitude and longitude:
            try:
                lat_val = float(latitude)
                lng_val = float(longitude)
            except ValueError:
                pass

        # Handle image upload to filesystem
        image_path = None
        if image and image.filename:
            if not allowed_file(image.filename):
                flash("Invalid image format. Allowed formats: PNG, JPG, JPEG, WebP.", "danger")
                return redirect(url_for("citizen.report_issue"))

            unique_filename = generate_unique_filename(image.filename)
            upload_folder = os.path.join(
                current_app.root_path, "static", "uploads", "complaint_images"
            )
            os.makedirs(upload_folder, exist_ok=True)
            save_path = os.path.join(upload_folder, unique_filename)

            try:
                image.save(save_path)
                image_path = f"uploads/complaint_images/{unique_filename}"
            except Exception as e:
                flash(f"Could not save uploaded photo: {str(e)}", "danger")
                return redirect(url_for("citizen.report_issue"))

        # Create complaint in Oracle
        success, result = ComplaintService.create_complaint(
            user_id=user_id,
            category_id=category_id,
            title=title,
            description=description,
            severity=severity,
            location=location,
            image_path=image_path
        )

        if not success:
            flash(f"Unable to submit complaint: {result}", "danger")
            return redirect(url_for("citizen.report_issue"))

        complaint_id = result

        # Record image metadata in COMPLAINT_IMAGES table
        if image_path:
            ComplaintImageModel.create_image(
                complaint_id=complaint_id,
                image_path=image_path,
                image_type="COMPLAINT"
            )

        # Update coordinates if provided
        if lat_val and lng_val:
            from database.connection import get_connection
            conn = get_connection()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute(
                        "UPDATE COMPLAINTS SET LATITUDE = :lat, LONGITUDE = :lng WHERE COMPLAINT_ID = :id",
                        {"lat": lat_val, "lng": lng_val, "id": complaint_id}
                    )
                    conn.commit()
                finally:
                    cur.close()
                    conn.close()

        # Day 20: Send email notification to citizen
        if user_email:
            NotificationService.notify_complaint_submitted(
                citizen_email=user_email,
                citizen_name=user_name,
                complaint_id=complaint_id,
                title=title
            )

        flash(f"Complaint #{complaint_id} submitted successfully.", "success")
        return redirect(url_for("citizen.my_complaints"))

    return render_template("citizen/report_issue.html")


# ==========================================
# My Complaints
# ==========================================

@citizen_bp.route("/my-complaints")
@login_required
@citizen_required
def my_complaints():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please login again.", "warning")
        return redirect(url_for("auth.login"))

    complaints = ComplaintService.get_user_complaints(user_id)
    return render_template(
        "citizen/my_complaints.html",
        complaints=complaints
    )


# ==========================================
# Day 19: Complete Complaint Tracking & Details
# ==========================================

@citizen_bp.route("/complaint/<int:complaint_id>")
@login_required
@citizen_required
def complaint_details(complaint_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("Please login again.", "warning")
        return redirect(url_for("auth.login"))

    # Fetch full details (includes worker name and resolution proof)
    complaint = ComplaintModel.get_complaint_full_details(complaint_id)
    if not complaint:
        flash("Complaint not found.", "danger")
        return redirect(url_for("citizen.my_complaints"))

    # Security Check: Ensure citizen owns this complaint
    if complaint[1] != user_id:
        flash("You do not have permission to view this complaint.", "danger")
        return redirect(url_for("citizen.my_complaints"))

    status_history = StatusHistoryModel.get_history_by_complaint(complaint_id)
    upvotes_count = ComplaintModel.get_upvotes_count(complaint_id)
    has_upvoted = ComplaintModel.has_user_upvoted(complaint_id, user_id)
    feedback = ComplaintModel.get_feedback_for_complaint(complaint_id)

    return render_template(
        "citizen/complaint_detail.html",
        complaint=complaint,
        status_history=status_history,
        upvotes_count=upvotes_count,
        has_upvoted=has_upvoted,
        feedback=feedback
    )


# ==========================================
# Day 22: Upvote Complaint
# ==========================================

@citizen_bp.route("/complaint/<int:complaint_id>/upvote", methods=["POST"])
@login_required
@citizen_required
def upvote_complaint(complaint_id):
    """Toggle upvote for a complaint."""
    user_id = session.get("user_id")
    has_upvoted, count = ComplaintModel.toggle_upvote(complaint_id, user_id)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"success": True, "has_upvoted": has_upvoted, "upvotes": count})

    flash("Upvote recorded!" if has_upvoted else "Upvote removed.", "success")
    return redirect(url_for("citizen.complaint_details", complaint_id=complaint_id))


# ==========================================
# Day 22: Citizen Resolution Feedback
# ==========================================

@citizen_bp.route("/complaint/<int:complaint_id>/feedback", methods=["POST"])
@login_required
@citizen_required
def submit_feedback(complaint_id):
    """Submit rating and feedback for a resolved complaint."""
    user_id = session.get("user_id")
    rating = request.form.get("rating", 5)
    comments = request.form.get("comments", "").strip()

    try:
        rating_int = int(rating)
        if not (1 <= rating_int <= 5):
            rating_int = 5
    except ValueError:
        rating_int = 5

    success, msg = ComplaintModel.submit_feedback(complaint_id, user_id, rating_int, comments)
    flash(msg, "success" if success else "danger")
    return redirect(url_for("citizen.complaint_details", complaint_id=complaint_id))