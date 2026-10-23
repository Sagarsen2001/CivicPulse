"""
=========================================
CivicPulse Application
=========================================

Main entry point of the CivicPulse
Smart Citizen Grievance Management System.

Author : Sagar Sen
Project : CivicPulse
"""

import os
from flask import Flask, render_template

from config import Config
from routes import public_bp, api_bp, auth_bp, citizen_bp
from routes.admin_routes import admin_bp
from routes.worker_routes import worker_bp

# ==========================================
# Create Flask Application
# ==========================================

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload storage directories exist
os.makedirs(os.path.join(app.root_path, "static", "uploads", "complaint_images"), exist_ok=True)
os.makedirs(os.path.join(app.root_path, "static", "uploads", "resolution_proofs"), exist_ok=True)


# ==========================================
# Register Blueprints
# ==========================================

app.register_blueprint(public_bp)
app.register_blueprint(api_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(citizen_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(worker_bp)


# ==========================================
# Day 26: Security Headers Middleware
# ==========================================

@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


# ==========================================
# Error Handlers
# ==========================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html"), 500


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)