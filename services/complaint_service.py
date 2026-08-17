"""
=========================================
CivicPulse Complaint Service
=========================================

Handles complaint business logic.

Author : Sagar Sen
Project: CivicPulse
"""

from models.complaint_model import ComplaintModel
from models.status_history_model import StatusHistoryModel


class ComplaintService:

    # ==========================================
    # Calculate Complaint Priority
    # ==========================================

    @staticmethod
    def calculate_priority(severity):

        if not severity:

            return "Low"

        severity = severity.strip().lower()

        if severity == "critical":

            return "High"

        if severity == "high":

            return "High"

        if severity == "medium":

            return "Medium"

        return "Low"

    # ==========================================
    # Create Complaint
    # ==========================================

    @staticmethod
    def create_complaint(
        user_id,
        category_id,
        title,
        description,
        severity,
        location,
        image_path=None
    ):
        """
        Create a complaint and automatically
        create its initial Pending status history.
        """

        # ==========================================
        # Calculate Priority
        # ==========================================

        priority = ComplaintService.calculate_priority(
            severity
        )

        # ==========================================
        # Create Complaint In Oracle
        # ==========================================

        success, result = ComplaintModel.create_complaint(

            user_id=user_id,

            category_id=category_id,

            title=title,

            description=description,

            severity=severity,

            location=location,

            image_path=image_path,

            priority=priority

        )

        # ==========================================
        # Complaint Creation Failed
        # ==========================================

        if not success:

            return False, result

        complaint_id = result

        # ==========================================
        # Create Initial Status History
        # ==========================================

        history_success, history_result = (
            StatusHistoryModel.create_history(

                complaint_id=complaint_id,

                old_status=None,

                new_status="Pending",

                changed_by=user_id,

                remarks=(
                    "Complaint submitted by citizen."
                )

            )
        )

        # ==========================================
        # History Creation Failed
        # ==========================================

        if not history_success:

            print(
                "⚠️ Complaint was created, "
                "but status history could not be created:"
            )

            print(history_result)

            # We do NOT delete the complaint here.
            # The complaint itself was successfully
            # created and can still be used.

        return True, complaint_id

    # ==========================================
    # Get Complaint By ID
    # ==========================================

    @staticmethod
    def get_complaint(complaint_id):

        return ComplaintModel.get_complaint_by_id(
            complaint_id
        )

    # ==========================================
    # Get All Complaints Of User
    # ==========================================

    @staticmethod
    def get_user_complaints(user_id):

        return ComplaintModel.get_complaints_by_user(
            user_id
        )

    # ==========================================
    # Get Complaint Summary
    # ==========================================

    @staticmethod
    def get_user_complaint_summary(user_id):

        return ComplaintModel.get_complaint_summary(
            user_id
        )

    # ==========================================
    # Get Recent Complaints
    # ==========================================

    @staticmethod
    def get_recent_user_complaints(
        user_id,
        limit=5
    ):

        return ComplaintModel.get_recent_complaints_by_user(

            user_id,

            limit

        )

    # ==========================================
    # Get Complete Dashboard Data
    # ==========================================

    @staticmethod
    def get_dashboard_data(user_id):

        summary = (
            ComplaintService.get_user_complaint_summary(
                user_id
            )
        )

        recent_complaints = (
            ComplaintService.get_recent_user_complaints(
                user_id,
                5
            )
        )

        return {

            "total_complaints": summary.get(
                "total",
                0
            ),

            "pending_complaints": summary.get(
                "pending",
                0
            ),

            "in_progress_complaints": summary.get(
                "in_progress",
                0
            ),

            "resolved_complaints": summary.get(
                "resolved",
                0
            ),

            "recent_complaints": recent_complaints

        }