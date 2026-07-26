"""
=========================================
CivicPulse Decorators
=========================================

Provides login and role based access.

Author : Sagar Sen
Project : CivicPulse
"""

from functools import wraps

from flask import session
from flask import redirect
from flask import url_for
from flask import flash


# ==========================================
# Login Required
# ==========================================

def login_required(view):

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:

            flash(

                "Please login first.",

                "warning"

            )

            return redirect(

                url_for(

                    "auth.login"

                )

            )

        return view(

            *args,

            **kwargs

        )

    return wrapped_view


# ==========================================
# Generic Role Required
# ==========================================

def role_required(role):

    def decorator(view):

        @wraps(view)
        def wrapped_view(*args, **kwargs):

            if "user_id" not in session:

                flash(

                    "Please login first.",

                    "warning"

                )

                return redirect(

                    url_for(

                        "auth.login"

                    )

                )

            if session.get("user_role") != role:

                flash(

                    "You are not authorized to access this page.",

                    "danger"

                )

                return redirect(

                    url_for(

                        "auth.unauthorized"

                    )

                )

            return view(

                *args,

                **kwargs

            )

        return wrapped_view

    return decorator


# ==========================================
# Citizen Required
# ==========================================

def citizen_required(view):

    return role_required(

        "Citizen"

    )(view)


# ==========================================
# Admin Required
# ==========================================

def admin_required(view):

    return role_required(

        "Admin"

    )(view)


# ==========================================
# Worker Required
# ==========================================

def worker_required(view):

    return role_required(

        "Worker"

    )(view)