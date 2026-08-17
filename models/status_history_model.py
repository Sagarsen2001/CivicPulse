"""
=========================================
CivicPulse Status History Model
=========================================

Handles database operations related to
complaint status history.

Author : Sagar Sen
Project: CivicPulse
"""

from database.connection import get_connection


class StatusHistoryModel:

    # ==========================================
    # Create Status History
    # ==========================================

    @staticmethod
    def create_history(
        complaint_id,
        new_status,
        changed_by=None,
        old_status=None,
        remarks=None
    ):
        """
        Create a new status history record.

        Parameters
        ----------
        complaint_id : int
            Complaint whose status changed.

        new_status : str
            New complaint status.

        changed_by : int, optional
            User who changed the status.

        old_status : str, optional
            Previous complaint status.

        remarks : str, optional
            Explanation for the status change.
        """

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if connection is None:
                return False, "Database connection failed."

            cursor = connection.cursor()

            sql = """
                INSERT INTO STATUS_HISTORY
                (
                    COMPLAINT_ID,
                    OLD_STATUS,
                    NEW_STATUS,
                    CHANGED_BY,
                    CHANGED_AT,
                    REMARKS
                )
                VALUES
                (
                    :complaint_id,
                    :old_status,
                    :new_status,
                    :changed_by,
                    CURRENT_TIMESTAMP,
                    :remarks
                )
            """

            cursor.execute(
                sql,
                {
                    "complaint_id": complaint_id,
                    "old_status": old_status,
                    "new_status": new_status,
                    "changed_by": changed_by,
                    "remarks": remarks
                }
            )

            connection.commit()

            return True, "Status history created successfully."

        except Exception as error:

            if connection:
                connection.rollback()

            print(
                "❌ Status History Creation Error:",
                error
            )

            return False, str(error)

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ==========================================
    # Get Status History By Complaint
    # ==========================================

    @staticmethod
    def get_history_by_complaint(complaint_id):

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if connection is None:
                return []

            cursor = connection.cursor()

            sql = """
                SELECT
                    HISTORY_ID,
                    COMPLAINT_ID,
                    OLD_STATUS,
                    NEW_STATUS,
                    CHANGED_BY,
                    CHANGED_AT,
                    REMARKS
                FROM STATUS_HISTORY
                WHERE COMPLAINT_ID = :complaint_id
                ORDER BY CHANGED_AT ASC
            """

            cursor.execute(
                sql,
                {
                    "complaint_id": complaint_id
                }
            )

            return cursor.fetchall()

        except Exception as error:

            print(
                "❌ Status History Error:",
                error
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ==========================================
    # Get Latest Status History
    # ==========================================

    @staticmethod
    def get_latest_status(complaint_id):

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if connection is None:
                return None

            cursor = connection.cursor()

            sql = """
                SELECT
                    HISTORY_ID,
                    COMPLAINT_ID,
                    OLD_STATUS,
                    NEW_STATUS,
                    CHANGED_BY,
                    CHANGED_AT,
                    REMARKS
                FROM STATUS_HISTORY
                WHERE COMPLAINT_ID = :complaint_id
                ORDER BY CHANGED_AT DESC
                FETCH FIRST 1 ROW ONLY
            """

            cursor.execute(
                sql,
                {
                    "complaint_id": complaint_id
                }
            )

            return cursor.fetchone()

        except Exception as error:

            print(
                "❌ Latest Status History Error:",
                error
            )

            return None

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()