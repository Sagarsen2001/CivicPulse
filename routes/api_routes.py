from flask import Blueprint
from flask import jsonify

from database.connection import get_connection


api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


@api_bp.route("/categories", methods=["GET"])
def get_categories():

    connection = get_connection()

    if connection is None:

        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            CATEGORY_ID,
            CATEGORY_NAME,
            DESCRIPTION
        FROM ISSUE_CATEGORIES
        ORDER BY CATEGORY_NAME
    """)

    categories = []

    for row in cursor.fetchall():

        categories.append({

            "category_id": row[0],
            "category_name": row[1],
            "description": row[2]

        })

    cursor.close()

    connection.close()

    return jsonify({

        "success": True,
        "categories": categories

    })