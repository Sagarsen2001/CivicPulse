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
                "[ERROR] Complaint Error:",
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
                "[ERROR] Recent Complaints Error:",
                error
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ==========================================
    # Get Complete Complaint Details (Joined)
    # ==========================================

    @staticmethod
    def get_complaint_full_details(complaint_id):
        """
        Get complaint with joined category, citizen, and assigned worker.
        """
        connection = get_connection()
        if connection is None:
            return None

        cursor = connection.cursor()
        try:
            sql = """
                SELECT
                    C.COMPLAINT_ID,
                    C.USER_ID,
                    C.CATEGORY_ID,
                    C.TITLE,
                    C.DESCRIPTION,
                    C.SEVERITY,
                    C.LOCATION,
                    C.IMAGE_PATH,
                    C.PRIORITY,
                    C.STATUS,
                    C.CREATED_AT,
                    C.UPDATED_AT,
                    C.ASSIGNED_TO,
                    C.RESOLUTION_PROOF,
                    C.RESOLVED_AT,
                    IC.CATEGORY_NAME,
                    U.FULL_NAME AS CITIZEN_NAME,
                    U.EMAIL AS CITIZEN_EMAIL,
                    U.PHONE_NUMBER AS CITIZEN_PHONE,
                    W.FULL_NAME AS WORKER_NAME,
                    W.EMAIL AS WORKER_EMAIL,
                    C.LATITUDE,
                    C.LONGITUDE
                FROM COMPLAINTS C
                JOIN ISSUE_CATEGORIES IC ON C.CATEGORY_ID = IC.CATEGORY_ID
                JOIN USERS U ON C.USER_ID = U.USER_ID
                LEFT JOIN USERS W ON C.ASSIGNED_TO = W.USER_ID
                WHERE C.COMPLAINT_ID = :complaint_id
            """
            cursor.execute(sql, {"complaint_id": complaint_id})
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    # ==========================================
    # Admin: Get All Complaints with Filtering
    # ==========================================

    @staticmethod
    def get_all_complaints_admin(status=None, category_id=None, priority=None, search=None):
        """
        Get all complaints with optional filtering for Admin view.
        """
        connection = get_connection()
        if connection is None:
            return []

        cursor = connection.cursor()
        try:
            sql = """
                SELECT
                    C.COMPLAINT_ID,
                    C.TITLE,
                    C.DESCRIPTION,
                    C.STATUS,
                    C.PRIORITY,
                    C.SEVERITY,
                    C.LOCATION,
                    C.CREATED_AT,
                    C.UPDATED_AT,
                    IC.CATEGORY_NAME,
                    U.FULL_NAME AS CITIZEN_NAME,
                    W.FULL_NAME AS WORKER_NAME,
                    C.IMAGE_PATH,
                    C.ASSIGNED_TO,
                    C.CATEGORY_ID
                FROM COMPLAINTS C
                JOIN ISSUE_CATEGORIES IC ON C.CATEGORY_ID = IC.CATEGORY_ID
                JOIN USERS U ON C.USER_ID = U.USER_ID
                LEFT JOIN USERS W ON C.ASSIGNED_TO = W.USER_ID
                WHERE 1=1
            """
            params = {}

            if status and status.lower() != 'all':
                sql += " AND LOWER(C.STATUS) = LOWER(:status)"
                params["status"] = status

            if category_id and str(category_id).lower() != 'all':
                sql += " AND C.CATEGORY_ID = :category_id"
                params["category_id"] = int(category_id)

            if priority and priority.lower() != 'all':
                sql += " AND LOWER(C.PRIORITY) = LOWER(:priority)"
                params["priority"] = priority

            if search and search.strip():
                sql += " AND (LOWER(C.TITLE) LIKE LOWER(:search) OR LOWER(C.LOCATION) LIKE LOWER(:search) OR LOWER(C.DESCRIPTION) LIKE LOWER(:search))"
                params["search"] = f"%{search.strip()}%"

            sql += " ORDER BY C.CREATED_AT DESC"
            cursor.execute(sql, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    # ==========================================
    # Admin: Assign Complaint to Worker
    # ==========================================

    @staticmethod
    def assign_to_worker(complaint_id, worker_id, assigned_by):
        """
        Assign complaint to worker, update status to 'Assigned', record history.
        """
        connection = get_connection()
        if connection is None:
            return False, "Database connection failed."

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT STATUS, TITLE, USER_ID FROM COMPLAINTS WHERE COMPLAINT_ID = :1", (complaint_id,))
            row = cursor.fetchone()
            if not row:
                return False, "Complaint not found."
            old_status = row[0]

            cursor.execute("SELECT FULL_NAME, EMAIL FROM USERS WHERE USER_ID = :1 AND ROLE = 'Worker'", (worker_id,))
            worker_row = cursor.fetchone()
            if not worker_row:
                return False, "Selected worker does not exist."
            worker_name = worker_row[0]

            cursor.execute("""
                UPDATE COMPLAINTS
                SET ASSIGNED_TO = :worker_id,
                    STATUS = 'Assigned',
                    UPDATED_AT = CURRENT_TIMESTAMP
                WHERE COMPLAINT_ID = :complaint_id
            """, {"worker_id": worker_id, "complaint_id": complaint_id})

            cursor.execute("""
                INSERT INTO STATUS_HISTORY
                    (COMPLAINT_ID, OLD_STATUS, NEW_STATUS, CHANGED_BY, CHANGED_AT, REMARKS)
                VALUES
                    (:complaint_id, :old_status, 'Assigned', :changed_by, CURRENT_TIMESTAMP, :remarks)
            """, {
                "complaint_id": complaint_id,
                "old_status": old_status,
                "changed_by": assigned_by,
                "remarks": f"Assigned to {worker_name}"
            })

            connection.commit()
            return True, f"Complaint successfully assigned to {worker_name}."
        except Exception as error:
            if connection:
                connection.rollback()
            return False, str(error)
        finally:
            cursor.close()
            connection.close()

    # ==========================================
    # Update Status (Generic / Worker / Admin)
    # ==========================================

    @staticmethod
    def update_complaint_status_with_history(complaint_id, new_status, changed_by, remarks='', resolution_proof=None):
        """
        Update status, record history, and set resolved_at / resolution_proof if resolving.
        """
        connection = get_connection()
        if connection is None:
            return False, "Database connection failed."

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT STATUS FROM COMPLAINTS WHERE COMPLAINT_ID = :1", (complaint_id,))
            res = cursor.fetchone()
            if not res:
                return False, "Complaint not found."
            old_status = res[0]

            if new_status == 'Resolved':
                if resolution_proof:
                    cursor.execute("""
                        UPDATE COMPLAINTS
                        SET STATUS = :new_status,
                            RESOLUTION_PROOF = :proof,
                            RESOLVED_AT = CURRENT_TIMESTAMP,
                            UPDATED_AT = CURRENT_TIMESTAMP
                        WHERE COMPLAINT_ID = :complaint_id
                    """, {"new_status": new_status, "proof": resolution_proof, "complaint_id": complaint_id})

                    cursor.execute("""
                        INSERT INTO COMPLAINT_IMAGES (COMPLAINT_ID, IMAGE_PATH, IMAGE_TYPE, UPLOADED_AT)
                        VALUES (:complaint_id, :proof, 'RESOLUTION', CURRENT_TIMESTAMP)
                    """, {"complaint_id": complaint_id, "proof": resolution_proof})
                else:
                    cursor.execute("""
                        UPDATE COMPLAINTS
                        SET STATUS = :new_status,
                            RESOLVED_AT = CURRENT_TIMESTAMP,
                            UPDATED_AT = CURRENT_TIMESTAMP
                        WHERE COMPLAINT_ID = :complaint_id
                    """, {"new_status": new_status, "complaint_id": complaint_id})
            else:
                cursor.execute("""
                    UPDATE COMPLAINTS
                    SET STATUS = :new_status,
                        UPDATED_AT = CURRENT_TIMESTAMP
                    WHERE COMPLAINT_ID = :complaint_id
                """, {"new_status": new_status, "complaint_id": complaint_id})

            cursor.execute("""
                INSERT INTO STATUS_HISTORY
                    (COMPLAINT_ID, OLD_STATUS, NEW_STATUS, CHANGED_BY, CHANGED_AT, REMARKS)
                VALUES
                    (:complaint_id, :old_status, :new_status, :changed_by, CURRENT_TIMESTAMP, :remarks)
            """, {
                "complaint_id": complaint_id,
                "old_status": old_status,
                "new_status": new_status,
                "changed_by": changed_by,
                "remarks": remarks or f"Status changed to {new_status}"
            })

            connection.commit()
            return True, f"Status updated to {new_status}."
        except Exception as error:
            if connection:
                connection.rollback()
            return False, str(error)
        finally:
            cursor.close()
            connection.close()

    # ==========================================
    # Admin: Update Priority
    # ==========================================

    @staticmethod
    def update_complaint_priority(complaint_id, priority, changed_by):
        """Update complaint priority with history record."""
        connection = get_connection()
        if connection is None:
            return False, "Database connection failed."

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT PRIORITY FROM COMPLAINTS WHERE COMPLAINT_ID = :1", (complaint_id,))
            row = cursor.fetchone()
            if not row:
                return False, "Complaint not found."
            old_priority = row[0]

            cursor.execute("""
                UPDATE COMPLAINTS
                SET PRIORITY = :priority,
                    UPDATED_AT = CURRENT_TIMESTAMP
                WHERE COMPLAINT_ID = :complaint_id
            """, {"priority": priority, "complaint_id": complaint_id})

            cursor.execute("""
                INSERT INTO STATUS_HISTORY
                    (COMPLAINT_ID, OLD_STATUS, NEW_STATUS, CHANGED_BY, CHANGED_AT, REMARKS)
                VALUES
                    (:complaint_id, NULL, NULL, :changed_by, CURRENT_TIMESTAMP, :remarks)
            """, {
                "complaint_id": complaint_id,
                "changed_by": changed_by,
                "remarks": f"Priority changed from {old_priority} to {priority}"
            })

            connection.commit()
            return True, f"Priority updated to {priority}."
        except Exception as error:
            if connection:
                connection.rollback()
            return False, str(error)
        finally:
            cursor.close()
            connection.close()

    # ==========================================
    # Worker: Get Assigned Complaints
    # ==========================================

    @staticmethod
    def get_complaints_by_worker(worker_id, status=None):
        """Get all complaints assigned to a specific worker."""
        connection = get_connection()
        if connection is None:
            return []

        cursor = connection.cursor()
        try:
            sql = """
                SELECT
                    C.COMPLAINT_ID,
                    C.TITLE,
                    C.DESCRIPTION,
                    C.STATUS,
                    C.PRIORITY,
                    C.SEVERITY,
                    C.LOCATION,
                    C.CREATED_AT,
                    C.UPDATED_AT,
                    IC.CATEGORY_NAME,
                    U.FULL_NAME AS CITIZEN_NAME,
                    C.IMAGE_PATH,
                    C.RESOLUTION_PROOF
                FROM COMPLAINTS C
                JOIN ISSUE_CATEGORIES IC ON C.CATEGORY_ID = IC.CATEGORY_ID
                JOIN USERS U ON C.USER_ID = U.USER_ID
                WHERE C.ASSIGNED_TO = :worker_id
            """
            params = {"worker_id": worker_id}

            if status and status.lower() != 'all':
                sql += " AND LOWER(C.STATUS) = LOWER(:status)"
                params["status"] = status

            sql += " ORDER BY CASE C.PRIORITY WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END, C.CREATED_AT DESC"
            cursor.execute(sql, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_worker_dashboard_summary(worker_id):
        """Get summary count for worker dashboard."""
        connection = get_connection()
        if connection is None:
            return {"total": 0, "assigned": 0, "in_progress": 0, "resolved": 0}

        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT
                    COUNT(*) AS TOTAL,
                    SUM(CASE WHEN STATUS = 'Assigned' THEN 1 ELSE 0 END) AS ASSIGNED,
                    SUM(CASE WHEN STATUS = 'In Progress' THEN 1 ELSE 0 END) AS IN_PROGRESS,
                    SUM(CASE WHEN STATUS = 'Resolved' THEN 1 ELSE 0 END) AS RESOLVED
                FROM COMPLAINTS
                WHERE ASSIGNED_TO = :worker_id
            """, {"worker_id": worker_id})
            row = cursor.fetchone()
            if row:
                return {
                    "total": row[0] or 0,
                    "assigned": row[1] or 0,
                    "in_progress": row[2] or 0,
                    "resolved": row[3] or 0
                }
            return {"total": 0, "assigned": 0, "in_progress": 0, "resolved": 0}
        finally:
            cursor.close()
            connection.close()

    # ==========================================
    # Day 22: Upvotes Operations
    # ==========================================

    @staticmethod
    def get_upvotes_count(complaint_id):
        """Get total upvote count for a complaint."""
        connection = get_connection()
        if connection is None:
            return 0
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM COMPLAINT_UPVOTES WHERE COMPLAINT_ID = :1", (complaint_id,))
            row = cursor.fetchone()
            return row[0] if row else 0
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def has_user_upvoted(complaint_id, user_id):
        """Check if user has already upvoted this complaint."""
        connection = get_connection()
        if connection is None:
            return False
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT 1 FROM COMPLAINT_UPVOTES WHERE COMPLAINT_ID = :1 AND USER_ID = :2", (complaint_id, user_id))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def toggle_upvote(complaint_id, user_id):
        """Toggle upvote for a user. Returns (has_upvoted: bool, count: int)."""
        connection = get_connection()
        if connection is None:
            return False, 0
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT UPVOTE_ID FROM COMPLAINT_UPVOTES WHERE COMPLAINT_ID = :1 AND USER_ID = :2", (complaint_id, user_id))
            row = cursor.fetchone()
            if row:
                cursor.execute("DELETE FROM COMPLAINT_UPVOTES WHERE COMPLAINT_ID = :1 AND USER_ID = :2", (complaint_id, user_id))
                has_upvoted = False
            else:
                cursor.execute("INSERT INTO COMPLAINT_UPVOTES (COMPLAINT_ID, USER_ID) VALUES (:1, :2)", (complaint_id, user_id))
                has_upvoted = True
            connection.commit()

            cursor.execute("SELECT COUNT(*) FROM COMPLAINT_UPVOTES WHERE COMPLAINT_ID = :1", (complaint_id,))
            count = cursor.fetchone()[0]
            return has_upvoted, count
        except Exception:
            if connection:
                connection.rollback()
            return False, 0
        finally:
            cursor.close()
            connection.close()

    # ==========================================
    # Day 22: Citizen Feedback Operations
    # ==========================================

    @staticmethod
    def submit_feedback(complaint_id, user_id, rating, comments=''):
        """Submit feedback for a resolved complaint."""
        connection = get_connection()
        if connection is None:
            return False, "Database connection failed."
        cursor = connection.cursor()
        try:
            # Check ownership and status
            cursor.execute("SELECT USER_ID, STATUS FROM COMPLAINTS WHERE COMPLAINT_ID = :1", (complaint_id,))
            row = cursor.fetchone()
            if not row:
                return False, "Complaint not found."
            if row[0] != user_id:
                return False, "You can only submit feedback for your own complaint."
            if row[1] != 'Resolved':
                return False, "Feedback can only be submitted for resolved complaints."

            # Check if feedback already exists
            cursor.execute("SELECT FEEDBACK_ID FROM COMPLAINT_FEEDBACK WHERE COMPLAINT_ID = :1", (complaint_id,))
            if cursor.fetchone():
                return False, "Feedback has already been submitted for this complaint."

            cursor.execute("""
                INSERT INTO COMPLAINT_FEEDBACK
                    (COMPLAINT_ID, USER_ID, RATING, COMMENTS, CREATED_AT)
                VALUES
                    (:complaint_id, :user_id, :rating, :comments, CURRENT_TIMESTAMP)
            """, {
                "complaint_id": complaint_id,
                "user_id": user_id,
                "rating": int(rating),
                "comments": comments
            })
            connection.commit()
            return True, "Feedback submitted successfully! Thank you."
        except Exception as error:
            if connection:
                connection.rollback()
            return False, str(error)
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_feedback_for_complaint(complaint_id):
        """Get feedback for a specific complaint."""
        connection = get_connection()
        if connection is None:
            return None
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT
                    F.FEEDBACK_ID,
                    F.COMPLAINT_ID,
                    F.USER_ID,
                    F.RATING,
                    F.COMMENTS,
                    F.CREATED_AT,
                    U.FULL_NAME AS CITIZEN_NAME
                FROM COMPLAINT_FEEDBACK F
                JOIN USERS U ON F.USER_ID = U.USER_ID
                WHERE F.COMPLAINT_ID = :1
            """, (complaint_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    # ==========================================
    # Day 24: Map Location Points
    # ==========================================

    @staticmethod
    def get_map_markers():
        """Get all complaints with coordinates for map display."""
        connection = get_connection()
        if connection is None:
            return []
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT
                    C.COMPLAINT_ID,
                    C.TITLE,
                    C.LATITUDE,
                    C.LONGITUDE,
                    C.STATUS,
                    C.PRIORITY,
                    C.LOCATION,
                    IC.CATEGORY_NAME
                FROM COMPLAINTS C
                JOIN ISSUE_CATEGORIES IC ON C.CATEGORY_ID = IC.CATEGORY_ID
                WHERE C.LATITUDE IS NOT NULL AND C.LONGITUDE IS NOT NULL
            """)
            rows = cursor.fetchall()
            return [
                {
                    "id": r[0],
                    "title": r[1],
                    "lat": float(r[2]),
                    "lng": float(r[3]),
                    "status": r[4],
                    "priority": r[5],
                    "location": r[6],
                    "category": r[7]
                }
                for r in rows
            ]
        finally:
            cursor.close()
            connection.close()