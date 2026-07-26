"""
=========================================
CivicPulse Application
=========================================

Main entry point of the application.

Author : Sagar Sen
Project : CivicPulse
"""

from flask import Flask
from flask import render_template

from config import Config

from routes import public_bp
from routes import api_bp
from routes import auth_bp
from routes import citizen_bp


# ==========================================
# Create Flask Application
# ==========================================

app = Flask(__name__)

app.config.from_object(Config)


# ==========================================
# Register Blueprints
# ==========================================

app.register_blueprint(public_bp)

app.register_blueprint(api_bp)

app.register_blueprint(auth_bp)

app.register_blueprint(citizen_bp)


# ==========================================
# Error Handlers
# ==========================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(

        "errors/404.html"

    ), 404


@app.errorhandler(500)
def internal_server_error(error):

    return render_template(

        "errors/500.html"

    ), 500


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":

    app.run(

        debug=True

    )