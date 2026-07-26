"""
=========================================
CivicPulse Authentication Routes
=========================================

Handles user registration,
login, logout, and session management.

Author : Sagar Sen
Project : CivicPulse
"""

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session

from services.auth_service import AuthService


auth_bp = Blueprint(

    "auth",

    __name__,

    url_prefix="/auth"

)


# ==========================================
# Register
# ==========================================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name")

        email = request.form.get("email")

        password = request.form.get("password")

        phone_number = request.form.get("phone_number")

        success, message = AuthService.register_user(

            full_name,

            email,

            password,

            phone_number

        )

        if success:

            flash(

                message,

                "success"

            )

            return redirect(

                url_for("auth.login")

            )

        flash(

            message,

            "danger"

        )

    return render_template(

        "auth/register.html"

    )


# ==========================================
# Login
# ==========================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")

        password = request.form.get("password")

        success, user, message = AuthService.login_user(

            email,

            password

        )

        if success:

            # ==========================
            # Store User Session
            # ==========================

            session["user_id"] = user[0]

            session["user_name"] = user[1]

            session["user_email"] = user[2]

            session["user_role"] = user[5]

            flash(

                message,

                "success"

            )

            # ==========================
            # Role Based Redirect
            # ==========================

            if user[5] == "Admin":

                return redirect(

                    url_for("public.home")

                )

            elif user[5] == "Worker":

                return redirect(

                    url_for("public.home")

                )

            else:

                return redirect(

                    url_for("public.home")

                )

        flash(

            message,

            "danger"

        )

    return render_template(

        "auth/login.html"

    )


# ==========================================
# Logout
# ==========================================

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash(

        "Logged out successfully.",

        "success"

    )

    return redirect(

        url_for("public.home")

    )


# ==========================================
# Unauthorized Page
# ==========================================

@auth_bp.route("/unauthorized")
def unauthorized():

    return render_template(

        "auth/unauthorized.html"

    )