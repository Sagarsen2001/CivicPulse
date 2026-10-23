"""
=========================================
CivicPulse Admin Routes
=========================================

Handles all administrator-related routes:
- Dashboard & Overview (Day 13)
- Complaint Management & Filtering (Day 14)
- Worker Assignment (Day 15)
- Priority Overrides (Day 23)
- Map View (Day 24)
- Analytics & CSV Export (Day 25)

Author : Sagar Sen
Project: CivicPulse
"""

import io
import csv
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    Response,
    jsonify
)

from utils.decorators import login_required, role_required
from services.analytics_service import AnalyticsService
from services.notification_service import NotificationService
from models.complaint_model import ComplaintModel
from models.user_model import UserModel
from models.status_history_model import StatusHistoryModel
from models.complaint_image_model import ComplaintImageModel
from database.connection import get_connection

# ==========================================
# Admin Blueprint
# ==========================================

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# ==========================================
# Day 13: Admin Dashboard
# ==========================================

@admin_bp.route("/dashboard")
@login_required
@role_required("Admin")
def dashboard():
    """Admin dashboard with high-level summary cards and charts."""
    dashboard_data = AnalyticsService.get_dashboard_data()
    return render_template(
        "admin/dashboard.html",
        dashboard_data=dashboard_data
    )


# ==========================================
# Day 14: Complaint Management & Filtering
# ==========================================

@admin_bp.route("/complaints")
@login_required
@role_required("Admin")
def complaints():
    """List all complaints with filtering by status, category, priority, and search."""
    status_filter = request.args.get("status", "all")
    category_filter = request.args.get("category_id", "all")
    priority_filter = request.args.get("priority", "all")
    search_query = request.args.get("search", "").strip()

    all_complaints = ComplaintModel.get_all_complaints_admin(
        status=status_filter if status_filter != "all" else None,
        category_id=category_filter if category_filter != "all" else None,
        priority=priority_filter if priority_filter != "all" else None,
        search=search_query if search_query else None
    )

    # Fetch categories for filter dropdown
    conn = get_connection()
    categories = []
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT CATEGORY_ID, CATEGORY_NAME FROM ISSUE_CATEGORIES ORDER BY CATEGORY_NAME")
        categories = cur.fetchall()
        cur.close()
        conn.close()

    return render_template(
        "admin/complaints.html",
        complaints=all_complaints,
        categories=categories,
        current_status=status_filter,
        current_category=category_filter,
        current_priority=priority_filter,
        search_query=search_query
    )


# ==========================================
# Complaint Details (Admin View)
# ==========================================

@admin_bp.route("/complaint/<int:complaint_id>")
@login_required
@role_required("Admin")
def complaint_detail(complaint_id):
    """View detailed information of a complaint, history, and available actions."""
    complaint = ComplaintModel.get_complaint_full_details(complaint_id)
    if not complaint:
        flash("Complaint not found.", "danger")
        return redirect(url_for("admin.complaints"))

    status_history = StatusHistoryModel.get_history_by_complaint(complaint_id)
    images = ComplaintImageModel.get_images_by_complaint(complaint_id)
    workers = UserModel.get_all_workers()
    upvotes_count = ComplaintModel.get_upvotes_count(complaint_id)
    feedback = ComplaintModel.get_feedback_for_complaint(complaint_id)

    return render_template(
        "admin/complaint_detail.html",
        complaint=complaint,
        status_history=status_history,
        images=images,
        workers=workers,
        upvotes_count=upvotes_count,
        feedback=feedback
    )


# ==========================================
# Day 14: Verify Complaint
# ==========================================

@admin_bp.route("/complaint/<int:complaint_id>/verify", methods=["POST"])
@login_required
@role_required("Admin")
def verify_complaint(complaint_id):
    """Verify a pending complaint."""
    admin_id = session.get("user_id")
    remarks = request.form.get("remarks", "Verified by Administrator").strip()

    success, msg = ComplaintModel.update_complaint_status_with_history(
        complaint_id=complaint_id,
        new_status="Verified",
        changed_by=admin_id,
        remarks=remarks
    )

    if success:
        flash("Complaint marked as Verified.", "success")
        # Notify citizen
        complaint = ComplaintModel.get_complaint_full_details(complaint_id)
        if complaint and complaint[17]:  # citizen email
            NotificationService.notify_status_changed(
                citizen_email=complaint[17],
                citizen_name=complaint[16],
                complaint_id=complaint_id,
                title=complaint[3],
                old_status="Pending",
                new_status="Verified"
            )
    else:
        flash(f"Error: {msg}", "danger")

    return redirect(url_for("admin.complaint_detail", complaint_id=complaint_id))


# ==========================================
# Day 14: Reject Complaint
# ==========================================

@admin_bp.route("/complaint/<int:complaint_id>/reject", methods=["POST"])
@login_required
@role_required("Admin")
def reject_complaint(complaint_id):
    """Reject a complaint with reason."""
    admin_id = session.get("user_id")
    remarks = request.form.get("remarks", "Rejected by Administrator").strip()

    if not remarks:
        flash("Please provide a reason for rejection.", "warning")
        return redirect(url_for("admin.complaint_detail", complaint_id=complaint_id))

    success, msg = ComplaintModel.update_complaint_status_with_history(
        complaint_id=complaint_id,
        new_status="Rejected",
        changed_by=admin_id,
        remarks=remarks
    )

    if success:
        flash("Complaint marked as Rejected.", "warning")
        complaint = ComplaintModel.get_complaint_full_details(complaint_id)
        if complaint and complaint[17]:
            NotificationService.notify_status_changed(
                citizen_email=complaint[17],
                citizen_name=complaint[16],
                complaint_id=complaint_id,
                title=complaint[3],
                old_status=complaint[9],
                new_status="Rejected"
            )
    else:
        flash(f"Error: {msg}", "danger")

    return redirect(url_for("admin.complaint_detail", complaint_id=complaint_id))


# ==========================================
# Day 15: Assign Complaint to Worker
# ==========================================

@admin_bp.route("/complaint/<int:complaint_id>/assign", methods=["POST"])
@login_required
@role_required("Admin")
def assign_complaint(complaint_id):
    """Assign complaint to a worker."""
    admin_id = session.get("user_id")
    worker_id = request.form.get("worker_id")

    if not worker_id:
        flash("Please select a worker to assign.", "warning")
        return redirect(url_for("admin.complaint_detail", complaint_id=complaint_id))

    try:
        worker_id = int(worker_id)
    except ValueError:
        flash("Invalid worker selected.", "danger")
        return redirect(url_for("admin.complaint_detail", complaint_id=complaint_id))

    success, msg = ComplaintModel.assign_to_worker(
        complaint_id=complaint_id,
        worker_id=worker_id,
        assigned_by=admin_id
    )

    if success:
        flash(msg, "success")
        # Trigger notifications
        complaint = ComplaintModel.get_complaint_full_details(complaint_id)
        if complaint:
            # Notify citizen
            if complaint[17]:
                NotificationService.notify_complaint_assigned(
                    citizen_email=complaint[17],
                    citizen_name=complaint[16],
                    complaint_id=complaint_id,
                    title=complaint[3],
                    worker_name=complaint[19]
                )
            # Notify worker
            if complaint[20]:
                NotificationService.notify_worker_assigned(
                    worker_email=complaint[20],
                    worker_name=complaint[19],
                    complaint_id=complaint_id,
                    title=complaint[3],
                    location=complaint[6]
                )
    else:
        flash(f"Assignment failed: {msg}", "danger")

    return redirect(url_for("admin.complaint_detail", complaint_id=complaint_id))


# ==========================================
# Day 23: Update Priority Override
# ==========================================

@admin_bp.route("/complaint/<int:complaint_id>/priority", methods=["POST"])
@login_required
@role_required("Admin")
def update_priority(complaint_id):
    """Override priority of a complaint."""
    admin_id = session.get("user_id")
    priority = request.form.get("priority", "Medium").strip()

    if priority not in ["Low", "Medium", "High", "Critical"]:
        flash("Invalid priority level selected.", "danger")
        return redirect(url_for("admin.complaint_detail", complaint_id=complaint_id))

    # Note: in schema, if constraint restricts to Low/Medium/High, map Critical to High
    if priority == "Critical":
        priority = "High"

    success, msg = ComplaintModel.update_complaint_priority(
        complaint_id=complaint_id,
        priority=priority,
        changed_by=admin_id
    )

    if success:
        flash(f"Priority successfully updated to {priority}.", "success")
    else:
        flash(f"Failed to update priority: {msg}", "danger")

    return redirect(url_for("admin.complaint_detail", complaint_id=complaint_id))


# ==========================================
# Day 15: Workers Workload Overview
# ==========================================

@admin_bp.route("/workers")
@login_required
@role_required("Admin")
def workers():
    """List all workers and their current workload."""
    workers_list = UserModel.get_all_workers()
    return render_template(
        "admin/workers.html",
        workers=workers_list
    )


# ==========================================
# Day 24: Interactive Map View
# ==========================================

@admin_bp.route("/map")
@login_required
@role_required("Admin")
def map_view():
    """Interactive Leaflet map showing all geo-tagged complaints."""
    markers = ComplaintModel.get_map_markers()
    return render_template(
        "admin/map.html",
        markers=markers
    )


# ==========================================
# Day 25: Advanced Analytics & Reports
# ==========================================

@admin_bp.route("/analytics")
@login_required
@role_required("Admin")
def analytics_reports():
    """Full analytics and reporting dashboard."""
    dashboard_data = AnalyticsService.get_dashboard_data()
    workers_list = UserModel.get_all_workers()

    # Get priority breakdown
    conn = get_connection()
    priority_stats = []
    if conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT PRIORITY, COUNT(*)
            FROM COMPLAINTS
            GROUP BY PRIORITY
            ORDER BY COUNT(*) DESC
        """)
        priority_stats = cur.fetchall()
        cur.close()
        conn.close()

    return render_template(
        "admin/analytics.html",
        dashboard_data=dashboard_data,
        workers=workers_list,
        priority_stats=priority_stats
    )


# ==========================================
# Day 25: CSV Export of Complaints
# ==========================================

@admin_bp.route("/export-csv")
@login_required
@role_required("Admin")
def export_csv():
    """Export complaints dataset to downloadable CSV."""
    complaints_data = ComplaintModel.get_all_complaints_admin()

    output = io.StringIO()
    writer = csv.writer(output)

    # Write headers
    writer.writerow([
        "Complaint ID",
        "Title",
        "Category",
        "Status",
        "Priority",
        "Severity",
        "Location",
        "Citizen Name",
        "Assigned Worker",
        "Created At",
        "Updated At"
    ])

    for row in complaints_data:
        writer.writerow([
            row[0],  # id
            row[1],  # title
            row[9],  # category name
            row[3],  # status
            row[4],  # priority
            row[5],  # severity
            row[6],  # location
            row[10], # citizen name
            row[11] or "Unassigned", # worker name
            row[7],  # created_at
            row[8]   # updated_at
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=civicpulse_complaints.csv"}
    )