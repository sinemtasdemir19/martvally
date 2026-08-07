from flask import Blueprint, jsonify, render_template, request

from app.database import add_lead, get_all_leads
from app.services.ai_service import AIServiceError, ai_service


# Blueprint for page routes
pages_bp = Blueprint(
    "pages",
    __name__,
)

# Blueprint for API routes
api_bp = Blueprint(
    "api",
    __name__,
)


# -----------------------------
# PAGE ROUTES
# -----------------------------

@pages_bp.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@pages_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


# -----------------------------
# CHAT API
# -----------------------------

@api_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}

    user_message = data.get("message", "").strip()
    history = data.get("history", [])

    if not user_message:
        return jsonify({
            "success": False,
            "error": "Message is required.",
        }), 400

    if not isinstance(history, list):
        return jsonify({
            "success": False,
            "error": "History must be a list.",
        }), 400

    try:
        answer = ai_service.generate_response(
            user_message=user_message,
            history=history,
        )

        return jsonify({
            "success": True,
            "answer": answer,
        }), 200

    except AIServiceError:
        return jsonify({
            "success": False,
            "error": (
                "The AI service is temporarily unavailable. "
                "Please try again later."
            ),
        }), 503


# -----------------------------
# CREATE LEAD API
# -----------------------------

@api_bp.route("/leads", methods=["POST"])
def create_lead():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()
    project_need = data.get("project_need", "").strip()

    if not name:
        return jsonify({
            "success": False,
            "error": "Name is required.",
        }), 400

    if not phone:
        return jsonify({
            "success": False,
            "error": "Phone is required.",
        }), 400

    try:
        lead_id = add_lead(
            name=name,
            phone=phone,
            email=email,
            message=message,
            project_need=project_need,
        )

        return jsonify({
            "success": True,
            "message": "Lead saved successfully.",
            "lead_id": lead_id,
        }), 201

    except Exception:
        return jsonify({
            "success": False,
            "error": "Unable to save the lead.",
        }), 500


# -----------------------------
# GET ALL LEADS API
# -----------------------------

@api_bp.route("/leads", methods=["GET"])
def list_leads():
    try:
        leads = get_all_leads()

        return jsonify({
            "success": True,
            "leads": leads,
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "error": "Unable to retrieve leads.",
        }), 500