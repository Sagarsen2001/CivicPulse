"""
=========================================
CivicPulse Notification Service
=========================================

Handles email notifications for complaint
lifecycle events.

Uses SMTP configuration from environment
variables. Gracefully degrades when SMTP
is not configured.

Author : Sagar Sen
Project: CivicPulse
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


class NotificationService:

    # ==========================================
    # SMTP Configuration
    # ==========================================

    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "noreply@civicpulse.com")
    SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "CivicPulse")

    @classmethod
    def is_configured(cls):
        """Check if SMTP is properly configured."""
        return bool(cls.SMTP_HOST and cls.SMTP_USER and cls.SMTP_PASSWORD)

    @classmethod
    def _send_email(cls, to_email, subject, html_body):
        """
        Send an email using SMTP.
        Returns (success: bool, message: str).
        """

        if not cls.is_configured():
            logger.info(
                "SMTP not configured. Email to %s skipped: %s",
                to_email, subject
            )
            return False, "SMTP not configured. Email delivery is disabled."

        if not to_email:
            return False, "No recipient email provided."

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{cls.SMTP_FROM_NAME} <{cls.SMTP_FROM_EMAIL}>"
            msg["To"] = to_email

            html_part = MIMEText(html_body, "html")
            msg.attach(html_part)

            with smtplib.SMTP(cls.SMTP_HOST, cls.SMTP_PORT) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(cls.SMTP_USER, cls.SMTP_PASSWORD)
                server.send_message(msg)

            logger.info(
                "Email sent to %s: %s", to_email, subject
            )
            return True, "Email sent successfully."

        except smtplib.SMTPException as error:
            logger.error(
                "SMTP error sending to %s: %s",
                to_email, str(error)
            )
            return False, f"SMTP error: {str(error)}"

        except Exception as error:
            logger.error(
                "Unexpected email error to %s: %s",
                to_email, str(error)
            )
            return False, f"Email error: {str(error)}"

    # ==========================================
    # Notification Templates
    # ==========================================

    @classmethod
    def notify_complaint_submitted(cls, citizen_email, citizen_name, complaint_id, title):
        """Notify citizen that their complaint was submitted."""

        subject = f"CivicPulse — Complaint #{complaint_id} Submitted"

        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
            <h2 style="color: #0f4c81;">Complaint Submitted Successfully</h2>
            <p>Dear {citizen_name},</p>
            <p>Your complaint has been submitted and is under review.</p>
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Complaint ID:</td>
                    <td style="padding: 8px;">#{complaint_id}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Title:</td>
                    <td style="padding: 8px;">{title}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Status:</td>
                    <td style="padding: 8px;">Pending</td>
                </tr>
            </table>
            <p>You will be notified when there are updates to your complaint.</p>
            <p style="color: #666; font-size: 12px;">— CivicPulse Team</p>
        </div>
        """

        return cls._send_email(citizen_email, subject, html)

    @classmethod
    def notify_complaint_assigned(cls, citizen_email, citizen_name, complaint_id, title, worker_name):
        """Notify citizen that their complaint was assigned to a worker."""

        subject = f"CivicPulse — Complaint #{complaint_id} Assigned"

        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
            <h2 style="color: #0f4c81;">Complaint Assigned</h2>
            <p>Dear {citizen_name},</p>
            <p>Your complaint <strong>#{complaint_id} — {title}</strong> has been
               assigned to <strong>{worker_name}</strong> for resolution.</p>
            <p>You will be notified when the status changes.</p>
            <p style="color: #666; font-size: 12px;">— CivicPulse Team</p>
        </div>
        """

        return cls._send_email(citizen_email, subject, html)

    @classmethod
    def notify_worker_assigned(cls, worker_email, worker_name, complaint_id, title, location):
        """Notify worker about a new assignment."""

        subject = f"CivicPulse — New Assignment: Complaint #{complaint_id}"

        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
            <h2 style="color: #0f4c81;">New Complaint Assignment</h2>
            <p>Dear {worker_name},</p>
            <p>You have been assigned a new complaint:</p>
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Complaint ID:</td>
                    <td style="padding: 8px;">#{complaint_id}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Title:</td>
                    <td style="padding: 8px;">{title}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Location:</td>
                    <td style="padding: 8px;">{location}</td>
                </tr>
            </table>
            <p>Please log in to your worker dashboard to view details and begin work.</p>
            <p style="color: #666; font-size: 12px;">— CivicPulse Team</p>
        </div>
        """

        return cls._send_email(worker_email, subject, html)

    @classmethod
    def notify_status_changed(cls, citizen_email, citizen_name, complaint_id, title, old_status, new_status):
        """Notify citizen of a status change."""

        subject = f"CivicPulse — Complaint #{complaint_id} Status Update"

        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
            <h2 style="color: #0f4c81;">Complaint Status Updated</h2>
            <p>Dear {citizen_name},</p>
            <p>Your complaint <strong>#{complaint_id} — {title}</strong> has been updated:</p>
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Previous Status:</td>
                    <td style="padding: 8px;">{old_status or 'N/A'}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">New Status:</td>
                    <td style="padding: 8px; color: #0f4c81; font-weight: bold;">{new_status}</td>
                </tr>
            </table>
            <p>Log in to CivicPulse to view the full details.</p>
            <p style="color: #666; font-size: 12px;">— CivicPulse Team</p>
        </div>
        """

        return cls._send_email(citizen_email, subject, html)

    @classmethod
    def notify_complaint_resolved(cls, citizen_email, citizen_name, complaint_id, title):
        """Notify citizen that their complaint has been resolved."""

        subject = f"CivicPulse — Complaint #{complaint_id} Resolved"

        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
            <h2 style="color: #28a745;">Complaint Resolved</h2>
            <p>Dear {citizen_name},</p>
            <p>Great news! Your complaint <strong>#{complaint_id} — {title}</strong>
               has been resolved.</p>
            <p>Please log in to view the resolution details and proof.
               We would appreciate your feedback on the resolution quality.</p>
            <p style="color: #666; font-size: 12px;">— CivicPulse Team</p>
        </div>
        """

        return cls._send_email(citizen_email, subject, html)

    # ==========================================
    # In-App Notification (Database)
    # ==========================================

    @classmethod
    def create_in_app_notification(cls, user_id, complaint_id, message):
        """Store an in-app notification in the database."""

        from database.connection import get_connection

        connection = None
        cursor = None

        try:
            connection = get_connection()
            if connection is None:
                return False

            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO NOTIFICATIONS
                    (USER_ID, COMPLAINT_ID, MESSAGE)
                VALUES
                    (:user_id, :complaint_id, :message)
            """, {
                "user_id": user_id,
                "complaint_id": complaint_id,
                "message": message
            })

            connection.commit()
            return True

        except Exception as error:
            if connection:
                connection.rollback()
            logger.error(
                "In-app notification error: %s", str(error)
            )
            return False

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def get_user_notifications(cls, user_id, limit=20):
        """Get recent notifications for a user."""

        from database.connection import get_connection

        connection = None
        cursor = None

        try:
            connection = get_connection()
            if connection is None:
                return []

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    NOTIFICATION_ID,
                    USER_ID,
                    COMPLAINT_ID,
                    MESSAGE,
                    IS_READ,
                    CREATED_AT
                FROM NOTIFICATIONS
                WHERE USER_ID = :user_id
                ORDER BY CREATED_AT DESC
                FETCH FIRST :limit ROWS ONLY
            """, {
                "user_id": user_id,
                "limit": limit
            })

            return cursor.fetchall()

        except Exception as error:
            logger.error(
                "Get notifications error: %s", str(error)
            )
            return []

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @classmethod
    def mark_notification_read(cls, notification_id, user_id):
        """Mark a notification as read."""

        from database.connection import get_connection

        connection = None
        cursor = None

        try:
            connection = get_connection()
            if connection is None:
                return False

            cursor = connection.cursor()

            cursor.execute("""
                UPDATE NOTIFICATIONS
                SET IS_READ = 1
                WHERE NOTIFICATION_ID = :notification_id
                AND USER_ID = :user_id
            """, {
                "notification_id": notification_id,
                "user_id": user_id
            })

            connection.commit()
            return True

        except Exception as error:
            if connection:
                connection.rollback()
            logger.error(
                "Mark notification read error: %s", str(error)
            )
            return False

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

