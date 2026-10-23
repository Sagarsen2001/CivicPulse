"""
=========================================
CivicPulse Worker Routes
=========================================

Handles all field worker-related routes:
- Worker Dashboard (Day 16)
- Complaint Details & Assignment Validation (Day 16)
- Status Transitions (Assigned -> In Progress -> Resolved) (Day 17)
- Resolution Proof Upload (Day 18)

Author : Sagar Sen
Project: CivicPulse
"""

import os
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app
)

from utils.decorators import login_required, worker_required
from utils.file_utils import allowed_file, generate_unique_filename
from services.notification_service import NotificationService
from models.complaint_model import ComplaintModel
from models.status_history_model import StatusHistoryModel
from models.complaint_image_model import ComplaintImageModel

# ==========================================
# Worker Blueprint
# ==========================================

worker_bp = Blueprint(
    "worker",
    __name__,
    url_prefix="/worker"
)


# ==========================================
# Day 16: Worker Dashboard
# ==========================================

@worker_bp.route("/dashboard")
@login_required
@worker_required
def dashboard():
    """Worker dashboard displaying assigned tasks and workload summary."""
    worker_id = session.get("user_id")
    status_filter = request.args.get("status", "all")

    summary = ComplaintModel.get_worker_dashboard_summary(worker_id)
    complaints = ComplaintModel.get_complaints_by_worker(
        worker_id,
        status=status_filter if status_filter != "all" else None
    )

    return render_template(
        "worker/dashboard.html",
        summary=summary,
        complaints=complaints,
        current_status=status_filter
    )


# ==========================================
# Day 16: View Assigned Complaint Details
# ==========================================

@worker_bp.route("/complaint/<int:complaint_id>")
@login_required
@worker_required
def complaint_detail(complaint_id):
    """View details of a complaint assigned to this worker."""
    worker_id = session.get("user_id")

    complaint = ComplaintModel.get_complaint_full_details(complaint_id)
    if not complaint:
        flash("Complaint not found.", "danger")
        return redirect(url_for("worker.dashboard"))

    # Security check: Worker must be assigned to this complaint
    if complaint[12] != worker_id:
        flash("You are not authorized to view this complaint.", "danger")
        return redirect(url_for("worker.dashboard"))

    status_history = StatusHistoryModel.get_history_by_complaint(complaint_id)
    images = ComplaintImageModel.get_images_by_complaint(complaint_id)

    # Determine allowable next statuses
    current_status = complaint[9]
    allowed_transitions = []
    if current_status == "Assigned":
        allowed_transitions = ["In Progress"]
    elif current_status == "In Progress":
        allowed_transitions = ["Resolved"]

    return render_template(
        "worker/complaint_detail.html",
        complaint=complaint,
        status_history=status_history,
        images=images,
        allowed_transitions=allowed_transitions
    )


# ==========================================
# Day 17 & 18: Update Status & Upload Proof
# ==========================================

@worker_bp.route("/complaint/<int:complaint_id>/update-status", methods=["POST"])
@login_required
@worker_required
def update_status(complaint_id):
    """Update complaint status and optionally attach resolution proof."""
    worker_id = session.get("user_id")

    complaint = ComplaintModel.get_complaint_full_details(complaint_id)
    if not complaint:
        flash("Complaint not found.", "danger")
        return redirect(url_for("worker.dashboard"))

    if complaint[12] != worker_id:
        flash("Unauthorized status update.", "danger")
        return redirect(url_for("worker.dashboard"))

    new_status = request.form.get("new_status", "").strip()
    remarks = request.form.get("remarks", "").strip()
    proof_file = request.files.get("resolution_proof")

    # Validate transition
    current_status = complaint[9]
    valid_transitions = {
        "Assigned": ["In Progress"],
        "In Progress": ["Resolved"]
    }

    if current_status not in valid_transitions or new_status not in valid_transitions[current_status]:
        flash(f"Invalid transition from '{current_status}' to '{new_status}'.", "danger")
        return redirect(url_for("worker.complaint_detail", complaint_id=complaint_id))

    # Handle resolution proof upload if status is changing to Resolved
    proof_path = None
    if new_status == "Resolved" and proof_file and proof_file.filename:
        if not allowed_file(proof_file.filename):
            flash("Invalid proof file format. Only JPG, PNG, and WebP are allowed.", "danger")
            return redirect(url_for("worker.complaint_detail", complaint_id=complaint_id))

        unique_name = generate_unique_filename(proof_file.filename)
        upload_folder = os.path.join(
            current_app.root_path,
            "static",
            "uploads",
            "resolution_proofs"
        )
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, unique_name)

        try:
            proof_file.save(file_path)
            proof_path = f"uploads/resolution_proofs/{unique_name}"
        except Exception as e:
            flash(f"Could not save proof image: {str(e)}", "danger")
            return redirect(url_for("worker.complaint_detail", complaint_id=complaint_id))

    success, msg = ComplaintModel.update_complaint_status_with_history(
        complaint_id=complaint_id,
        new_status=new_status,
        changed_by=worker_id,
        remarks=remarks or f"Progress updated by worker to {new_status}",
        resolution_proof=proof_path
    )

    if success:
        flash(f"Complaint successfully updated to '{new_status}'.", "success")

        # Notify citizen
        if complaint[17]:  # citizen email
            if new_status == "Resolved":
                NotificationService.notify_complaint_resolved(
                    citizen_email=complaint[17],
                    citizen_name=complaint[16],
                    complaint_id=complaint_id,
                    title=complaint[3]
                )
            else:
                NotificationService.notify_status_changed(
                    citizen_email=complaint[17],
                    citizen_name=complaint[16],
                    complaint_id=complaint_id,
                    title=complaint[3],
                    old_status=current_status,
                    new_status=new_status
                )
    else:
        flash(f"Failed to update status: {msg}", "danger")

    return redirect(url_for("worker.complaint_detail", complaint_id=complaint_id))


# ==========================================
# Day 18: Upload Standalone Resolution Proof
# ==========================================

@worker_bp.route("/complaint/<int:complaint_id>/upload-proof", methods=["POST"])
@login_required
@worker_required
def upload_proof(complaint_id):
    """Upload resolution proof photographic evidence."""
    worker_id = session.get("user_id")

    complaint = ComplaintModel.get_complaint_full_details(complaint_id)
    if not complaint:
        flash("Complaint not found.", "danger")
        return redirect(url_for("worker.dashboard"))

    if complaint[12] != worker_id:
        flash("Unauthorized upload attempt.", "danger")
        return redirect(url_for("worker.dashboard"))

    proof_file = request.files.get("resolution_proof")
    if not proof_file or not proof_file.filename:
        flash("Please select an image file to upload as proof.", "warning")
        return redirect(url_for("worker.complaint_detail", complaint_id=complaint_id))

    if not allowed_file(proof_file.filename):
        flash("Invalid file format. Please upload JPG, PNG, or WebP images.", "danger")
        return redirect(url_for("worker.complaint_detail", complaint_id=complaint_id))

    unique_name = generate_unique_filename(proof_file.filename)
    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "resolution_proofs"
    )
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, unique_name)

    try:
        proof_file.save(file_path)
        proof_path = f"uploads/resolution_proofs/{unique_name}"
    except Exception as e:
        flash(f"Failed to save image file: {str(e)}", "danger")
        return redirect(url_for("worker.complaint_detail", complaint_id=complaint_id))

    # Update complaint resolution proof and record image
    from database.connection import get_connection
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE COMPLAINTS
                SET RESOLUTION_PROOF = :proof,
                    UPDATED_AT = CURRENT_TIMESTAMP
                WHERE COMPLAINT_ID = :complaint_id
            """, {"proof": proof_path, "complaint_id": complaint_id})

            cur.execute("""
                INSERT INTO COMPLAINT_IMAGES (COMPLAINT_ID, IMAGE_PATH, IMAGE_TYPE, UPLOADED_AT)
                VALUES (:complaint_id, :proof, 'RESOLUTION', CURRENT_TIMESTAMP)
            """, {"complaint_id": complaint_id, "proof": proof_path})

            conn.commit()
            flash("Resolution proof photo uploaded successfully.", "success")
        except Exception as error:
            conn.rollback()
            flash(f"Database error saving proof: {str(error)}", "danger")
        finally:
            cur.close()
            conn.close()

    return redirect(url_for("worker.complaint_detail", complaint_id=complaint_id))

