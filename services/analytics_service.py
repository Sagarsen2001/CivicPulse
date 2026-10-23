"""
=========================================
CivicPulse Analytics Service
=========================================

Handles analytics and statistics required
for the Admin Dashboard.

Author : Sagar Sen
Project: CivicPulse
"""

from database.connection import get_connection


class AnalyticsService:

    # ==========================================
    # Get Complaint Statistics
    # ==========================================

    @staticmethod
    def get_complaint_statistics():

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if connection is None:
                return {
                    "total": 0,
                    "pending": 0,
                    "verified": 0,
                    "assigned": 0,
                    "in_progress": 0,
                    "resolved": 0,
                    "rejected": 0
                }

            cursor = connection.cursor()

            sql = """
                SELECT
                    COUNT(*) AS TOTAL,

                    SUM(
                        CASE
                            WHEN STATUS = 'Pending'
                            THEN 1
                            ELSE 0
                        END
                    ) AS PENDING,

                    SUM(
                        CASE
                            WHEN STATUS = 'Verified'
                            THEN 1
                            ELSE 0
                        END
                    ) AS VERIFIED,

                    SUM(
                        CASE
                            WHEN STATUS = 'Assigned'
                            THEN 1
                            ELSE 0
                        END
                    ) AS ASSIGNED,

                    SUM(
                        CASE
                            WHEN STATUS = 'In Progress'
                            THEN 1
                            ELSE 0
                        END
                    ) AS IN_PROGRESS,

                    SUM(
                        CASE
                            WHEN STATUS = 'Resolved'
                            THEN 1
                            ELSE 0
                        END
                    ) AS RESOLVED,

                    SUM(
                        CASE
                            WHEN STATUS = 'Rejected'
                            THEN 1
                            ELSE 0
                        END
                    ) AS REJECTED

                FROM COMPLAINTS
            """

            cursor.execute(sql)

            row = cursor.fetchone()

            if row is None:
                return {
                    "total": 0,
                    "pending": 0,
                    "verified": 0,
                    "assigned": 0,
                    "in_progress": 0,
                    "resolved": 0,
                    "rejected": 0
                }

            return {
                "total": row[0] or 0,
                "pending": row[1] or 0,
                "verified": row[2] or 0,
                "assigned": row[3] or 0,
                "in_progress": row[4] or 0,
                "resolved": row[5] or 0,
                "rejected": row[6] or 0
            }

        except Exception as error:

            print(
                "❌ Analytics Error:",
                error
            )

            return {
                "total": 0,
                "pending": 0,
                "verified": 0,
                "assigned": 0,
                "in_progress": 0,
                "resolved": 0,
                "rejected": 0
            }

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ==========================================
    # Complaint Statistics For Chart
    # ==========================================

    @staticmethod
    def get_status_chart_data():

        statistics = (
            AnalyticsService.get_complaint_statistics()
        )

        return {
            "labels": [
                "Pending",
                "Verified",
                "Assigned",
                "In Progress",
                "Resolved",
                "Rejected"
            ],

            "values": [
                statistics["pending"],
                statistics["verified"],
                statistics["assigned"],
                statistics["in_progress"],
                statistics["resolved"],
                statistics["rejected"]
            ]
        }

    # ==========================================
    # Get Category-wise Complaint Count
    # ==========================================

    @staticmethod
    def get_category_statistics():

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if connection is None:
                return []

            cursor = connection.cursor()

            sql = """
                SELECT
                    IC.CATEGORY_NAME,
                    COUNT(C.COMPLAINT_ID) AS COMPLAINT_COUNT

                FROM ISSUE_CATEGORIES IC

                LEFT JOIN COMPLAINTS C
                    ON IC.CATEGORY_ID = C.CATEGORY_ID

                GROUP BY
                    IC.CATEGORY_ID,
                    IC.CATEGORY_NAME

                ORDER BY
                    COMPLAINT_COUNT DESC
            """

            cursor.execute(sql)

            rows = cursor.fetchall()

            return [
                {
                    "category": row[0],
                    "count": row[1]
                }
                for row in rows
            ]

        except Exception as error:

            print(
                "❌ Category Analytics Error:",
                error
            )

            return []

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ==========================================
    # Get Complete Admin Dashboard Data
    # ==========================================

    @staticmethod
    def get_dashboard_data():

        statistics = (
            AnalyticsService.get_complaint_statistics()
        )

        status_chart = (
            AnalyticsService.get_status_chart_data()
        )

        category_statistics = (
            AnalyticsService.get_category_statistics()
        )

        return {
            "statistics": statistics,
            "status_chart": status_chart,
            "category_statistics": category_statistics
        }