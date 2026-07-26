"""
=========================================
CivicPulse Public Routes
=========================================

Contains all public routes.

Author : Sagar Sen
Project : CivicPulse
"""

from flask import Blueprint
from flask import render_template

from utils.decorators import login_required


public_bp = Blueprint(

    "public",

    __name__

)


# ==========================================
# Home
# ==========================================

@public_bp.route("/")
def home():

    return render_template(

        "public/home.html"

    )


# ==========================================
# About
# ==========================================

@public_bp.route("/about")
def about():

    return render_template(

        "public/about.html"

    )


# ==========================================
# How It Works
# ==========================================

@public_bp.route("/how-it-works")
def how_it_works():

    return render_template(

        "public/how_it_works.html"

    )


# ==========================================
# Categories
# ==========================================

@public_bp.route("/categories")
def categories():

    return render_template(

        "public/categories.html"

    )


# ==========================================
# User Dashboard
# ==========================================

@login_required
@public_bp.route("/dashboard")
def dashboard():

    return render_template(

        "public/home.html"

    )


# ==========================================
# User Profile
# ==========================================

@login_required
@public_bp.route("/profile")
def profile():

    return render_template(

        "public/home.html"

    )