"""
=========================================
CivicPulse Citizen Routes
=========================================

Handles all citizen-related pages.

Author : Sagar Sen
Project: CivicPulse
"""

from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session

from utils.decorators import login_required
from utils.decorators import citizen_required

from services.validation_service import ValidationService
from services.complaint_service import ComplaintService

from models.status_history_model import StatusHistoryModel


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

        flash(
            "Please login again.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    dashboard_data = ComplaintService.get_dashboard_data(
        user_id
    )

    return render_template(
        "citizen/dashboard.html",
        **dashboard_data
    )


# ==========================================
# Report Issue
# ==========================================

@citizen_bp.route(
    "/report-issue",
    methods=["GET", "POST"]
)
@login_required
@citizen_required
def report_issue():

    if request.method == "POST":

        user_id = session.get("user_id")

        if not user_id:

            flash(
                "User session not found. Please login again.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        title = request.form.get(
            "title",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        severity = request.form.get(
            "severity",
            ""
        ).strip()

        location = request.form.get(
            "location",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        image = request.files.get(
            "image"
        )

        # ==========================================
        # Validate Complaint
        # ==========================================

        errors = ValidationService.validate_complaint(
            title,
            category,
            severity,
            location,
            description
        )

        if errors:

            for error in errors:

                flash(
                    error,
                    "danger"
                )

            return redirect(
                url_for(
                    "citizen.report_issue"
                )
            )

        # ==========================================
        # Convert Category ID
        # ==========================================

        try:

            category_id = int(category)

        except (TypeError, ValueError):

            flash(
                "Invalid complaint category.",
                "danger"
            )

            return redirect(
                url_for(
                    "citizen.report_issue"
                )
            )

        # ==========================================
        # Image Path
        # ==========================================

        image_path = None

        if image and image.filename:

            image_path = image.filename

        # ==========================================
        # Create Complaint
        # ==========================================

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

            flash(
                f"Unable to submit complaint: {result}",
                "danger"
            )

            return redirect(
                url_for(
                    "citizen.report_issue"
                )
            )

        complaint_id = result

        flash(
            f"Complaint #{complaint_id} submitted successfully.",
            "success"
        )

        return redirect(
            url_for(
                "citizen.my_complaints"
            )
        )

    return render_template(
        "citizen/report_issue.html"
    )


# ==========================================
# My Complaints
# ==========================================

@citizen_bp.route("/my-complaints")
@login_required
@citizen_required
def my_complaints():

    user_id = session.get("user_id")

    if not user_id:

        flash(
            "Please login again.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    complaints = ComplaintService.get_user_complaints(
        user_id
    )

    return render_template(
        "citizen/my_complaints.html",
        complaints=complaints
    )


# ==========================================
# Complaint Details
# ==========================================

@citizen_bp.route(
    "/complaint/<int:complaint_id>"
)
@login_required
@citizen_required
def complaint_details(complaint_id):

    user_id = session.get("user_id")

    if not user_id:

        flash(
            "Please login again.",
            "warning"
        )

        return redirect(
            url_for("auth.login")
        )

    # ==========================================
    # Get Complaint
    # ==========================================

    complaint = ComplaintService.get_complaint(
        complaint_id
    )

    if not complaint:

        flash(
            "Complaint not found.",
            "danger"
        )

        return redirect(
            url_for(
                "citizen.my_complaints"
            )
        )

    # ==========================================
    # Security Check
    # ==========================================

    complaint_user_id = complaint[1]

    if complaint_user_id != user_id:

        flash(
            "You do not have permission to view this complaint.",
            "danger"
        )

        return redirect(
            url_for(
                "citizen.my_complaints"
            )
        )

    # ==========================================
    # Get Status History
    # ==========================================

    status_history = (
        StatusHistoryModel.get_history_by_complaint(
            complaint_id
        )
    )

    # ==========================================
    # Render Complaint Detail
    # ==========================================

    return render_template(
        "citizen/complaint_detail.html",
        complaint=complaint,
        status_history=status_history
    )