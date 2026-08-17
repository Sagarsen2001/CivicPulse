"""
=========================================
CivicPulse Complaint Image Model
=========================================

Handles database operations for complaint
image metadata.

Author : Sagar Sen
Project: CivicPulse
"""

from database.connection import get_connection


class ComplaintImageModel:

    # ==========================================
    # Save Image Metadata
    # ==========================================

    @staticmethod
    def create_image(
        complaint_id,
        image_path,
        image_type="COMPLAINT"
    ):
        """
        Store complaint image metadata in Oracle.

        image_type:
            COMPLAINT   -> Citizen uploaded image
            RESOLUTION  -> Worker resolution proof
        """

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if connection is None:
                return False, "Database connection failed."

            cursor = connection.cursor()

            sql = """
                INSERT INTO COMPLAINT_IMAGES
                (
                    COMPLAINT_ID,
                    IMAGE_PATH,
                    IMAGE_TYPE,
                    UPLOADED_AT
                )
                VALUES
                (
                    :complaint_id,
                    :image_path,
                    :image_type,
                    CURRENT_TIMESTAMP
                )
            """

            cursor.execute(
                sql,
                {
                    "complaint_id": complaint_id,
                    "image_path": image_path,
                    "image_type": image_type
                }
            )

            connection.commit()

            return True, "Image metadata saved successfully."

        except Exception as error:

            if connection:
                connection.rollback()

            print(
                "❌ Complaint Image Error:",
                error
            )

            return False, str(error)

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()


    # ==========================================
    # Get Images By Complaint
    # ==========================================

    @staticmethod
    def get_images_by_complaint(complaint_id):

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if connection is None:
                return []

            cursor = connection.cursor()

            sql = """
                SELECT
                    IMAGE_ID,
                    COMPLAINT_ID,
                    IMAGE_PATH,
                    IMAGE_TYPE,
                    UPLOADED_AT
                FROM COMPLAINT_IMAGES
                WHERE COMPLAINT_ID = :complaint_id
                ORDER BY UPLOADED_AT DESC
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
                "❌ Get Complaint Images Error:",
                error
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()