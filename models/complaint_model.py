"""
=========================================
CivicPulse Complaint Model
=========================================

Handles all database operations related
to civic complaints.

Author : Sagar Sen
Project: CivicPulse
"""

from database.connection import get_connection


class ComplaintModel:

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
        image_path=None,
        priority=None
    ):

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if connection is None:
                return False, "Database connection failed."

            cursor = connection.cursor()

            sql = """
                INSERT INTO COMPLAINTS
                (
                    USER_ID,
                    CATEGORY_ID,
                    TITLE,
                    DESCRIPTION,
                    SEVERITY,
                    LOCATION,
                    IMAGE_PATH,
                    PRIORITY,
                    STATUS
                )
                VALUES
                (
                    :user_id,
                    :category_id,
                    :title,
                    :description,
                    :severity,
                    :location,
                    :image_path,
                    :priority,
                    'Pending'
                )
                RETURNING COMPLAINT_ID INTO :complaint_id
            """

            complaint_id = cursor.var(int)

            cursor.execute(
                sql,
                {
                    "user_id": user_id,
                    "category_id": category_id,
                    "title": title,
                    "description": description,
                    "severity": severity,
                    "location": location,
                    "image_path": image_path,
                    "priority": priority,
                    "complaint_id": complaint_id
                }
            )

            connection.commit()

            generated_id = complaint_id.getvalue()[0]

            return True, generated_id

        except Exception as error:

            if connection:
                connection.rollback()

            print(
                "❌ Complaint Creation Error:",
                error
            )

            return False, str(error)

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


    # ==========================================
    # Get Complaint By ID
    # ==========================================

    @staticmethod
    def get_complaint_by_id(complaint_id):

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if connection is None:
                return None

            cursor = connection.cursor()

            sql = """
                SELECT
                    COMPLAINT_ID,
                    USER_ID,
                    CATEGORY_ID,
                    TITLE,
                    DESCRIPTION,
                    SEVERITY,
                    LOCATION,
                    IMAGE_PATH,
                    PRIORITY,
                    STATUS,
                    CREATED_AT,
                    UPDATED_AT
                FROM COMPLAINTS
                WHERE COMPLAINT_ID = :complaint_id
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
                "❌ Get Complaint Error:",
                error
            )

            return None

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


    # ==========================================
    # Get Complaints By User
    # ==========================================

    @staticmethod
    def get_complaints_by_user(user_id):

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if connection is None:
                return []

            cursor = connection.cursor()

            sql = """
                SELECT
                    COMPLAINT_ID,
                    USER_ID,
                    CATEGORY_ID,
                    TITLE,
                    DESCRIPTION,
                    SEVERITY,
                    LOCATION,
                    IMAGE_PATH,
                    PRIORITY,
                    STATUS,
                    CREATED_AT,
                    UPDATED_AT
                FROM COMPLAINTS
                WHERE USER_ID = :user_id
                ORDER BY CREATED_AT DESC
            """

            cursor.execute(
                sql,
                {
                    "user_id": user_id
                }
            )

            return cursor.fetchall()

        except Exception as error:

            print(
                "❌ Get User Complaints Error:",
                error
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


    # ==========================================
    # Get Complaint Summary
    # ==========================================

    @staticmethod
    def get_complaint_summary(user_id):

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if connection is None:

                return {
                    "total": 0,
                    "pending": 0,
                    "in_progress": 0,
                    "resolved": 0
                }

            cursor = connection.cursor()

            sql = """
                SELECT
                    COUNT(*) AS TOTAL_COMPLAINTS,

                    NVL(
                        SUM(
                            CASE
                                WHEN STATUS = 'Pending'
                                THEN 1
                                ELSE 0
                            END
                        ),
                        0
                    ) AS PENDING_COMPLAINTS,

                    NVL(
                        SUM(
                            CASE
                                WHEN STATUS = 'In Progress'
                                THEN 1
                                ELSE 0
                            END
                        ),
                        0
                    ) AS IN_PROGRESS_COMPLAINTS,

                    NVL(
                        SUM(
                            CASE
                                WHEN STATUS = 'Resolved'
                                THEN 1
                                ELSE 0
                            END
                        ),
                        0
                    ) AS RESOLVED_COMPLAINTS

                FROM COMPLAINTS
                WHERE USER_ID = :user_id
            """

            cursor.execute(
                sql,
                {
                    "user_id": user_id
                }
            )

            row = cursor.fetchone()

            if row is None:

                return {
                    "total": 0,
                    "pending": 0,
                    "in_progress": 0,
                    "resolved": 0
                }

            return {
                "total": row[0] or 0,
                "pending": row[1] or 0,
                "in_progress": row[2] or 0,
                "resolved": row[3] or 0
            }

        except Exception as error:

            print(
                "❌ Complaint Summary Error:",
                error
            )

            return {
                "total": 0,
                "pending": 0,
                "in_progress": 0,
                "resolved": 0
            }

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


    # ==========================================
    # Get Recent Complaints By User
    # ==========================================

    @staticmethod
    def get_recent_complaints_by_user(
        user_id,
        limit=5
    ):

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if connection is None:
                return []

            cursor = connection.cursor()

            # Use a controlled integer value for FETCH FIRST.
            safe_limit = max(1, min(int(limit), 20))

            sql = f"""
                SELECT
                    COMPLAINT_ID,
                    USER_ID,
                    CATEGORY_ID,
                    TITLE,
                    DESCRIPTION,
                    SEVERITY,
                    LOCATION,
                    IMAGE_PATH,
                    PRIORITY,
                    STATUS,
                    CREATED_AT,
                    UPDATED_AT
                FROM COMPLAINTS
                WHERE USER_ID = :user_id
                ORDER BY CREATED_AT DESC
                FETCH FIRST {safe_limit} ROWS ONLY
            """

            cursor.execute(
                sql,
                {
                    "user_id": user_id
                }
            )

            return cursor.fetchall()

        except Exception as error:

            print(
                "❌ Recent Complaints Error:",
                error
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()