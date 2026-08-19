from flask import Flask, jsonify
from flask_cors import CORS

from configs import config_by_name
from app.database import close_db, init_db
from app.routes import api_bp, pages_bp


def create_app(config_name="development"):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_by_name[config_name])

    # Enable CORS
    CORS(
        app,
        origins=app.config["CORS_ORIGINS"],
    )

    # Initialize database
    init_db(app)

    # Close database connection after each request
    app.teardown_appcontext(close_db)

    # Register page routes
    app.register_blueprint(pages_bp)

    # Register API routes with /api prefix
    app.register_blueprint(
        api_bp,
        url_prefix="/api",
    )

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "active",
            "service": "martvally-api",
        }), 200

    return app