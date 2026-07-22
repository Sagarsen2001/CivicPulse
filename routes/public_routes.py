from flask import Blueprint, render_template

# ==========================================
# Public Blueprint
# ==========================================

public_bp = Blueprint(
    "public",
    __name__
)

# ==========================================
# Home Page
# ==========================================

@public_bp.route("/")
def home():
    return render_template("public/home.html")


# ==========================================
# About Page
# ==========================================

@public_bp.route("/about")
def about():
    return render_template("public/about.html")


# ==========================================
# How It Works Page
# ==========================================

@public_bp.route("/how-it-works")
def how_it_works():
    return render_template("public/how_it_works.html")

@public_bp.route("/categories")
def categories():

    return render_template("public/categories.html")