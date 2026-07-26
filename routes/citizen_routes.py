"""
=========================================
CivicPulse Citizen Routes
=========================================

Handles all citizen-related pages.

Author : Sagar Sen
Project : CivicPulse
"""

from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for

from utils.decorators import login_required
from utils.decorators import citizen_required

from services.validation_service import ValidationService


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

    return render_template(

        "public/home.html"

    )


# ==========================================
# Report Issue
# ==========================================

@citizen_bp.route("/report-issue", methods=["GET", "POST"])
@login_required
@citizen_required
def report_issue():

    if request.method == "POST":

        title = request.form.get("title", "").strip()

        category = request.form.get("category", "").strip()

        severity = request.form.get("severity", "").strip()

        location = request.form.get("location", "").strip()

        description = request.form.get("description", "").strip()

        image = request.files.get("image")

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
        # Database Logic
        # (Will be added in upcoming days)
        # ==========================================

        flash(

            "Complaint submitted successfully (Demo).",

            "success"

        )

        return redirect(

            url_for(

                "citizen.report_issue"

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

    flash(

        "Complaint history will be available in upcoming days.",

        "info"

    )

    return redirect(

        url_for(

            "citizen.report_issue"

        )

    )


# ==========================================
# Complaint Details
# ==========================================

@citizen_bp.route("/complaint/<int:complaint_id>")
@login_required
@citizen_required
def complaint_details(

    complaint_id

):

    flash(

        f"Complaint #{complaint_id} details will be available in upcoming days.",

        "info"

    )

    return redirect(

        url_for(

            "citizen.report_issue"

        )

    )