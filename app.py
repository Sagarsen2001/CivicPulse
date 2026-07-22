from flask import Flask, render_template

from config import Config

# Import Blueprints
from routes import public_bp
from routes import api_bp


# ==========================================
# Create Flask Application
# ==========================================

app = Flask(__name__)

# Load Configuration
app.config.from_object(Config)


# ==========================================
# Register Blueprints
# ==========================================

app.register_blueprint(public_bp)

app.register_blueprint(api_bp)


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
        host="127.0.0.1",
        port=5000,
        debug=True
    )