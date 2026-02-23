from flask import Blueprint, request, jsonify
import sqlite3

save_ai_bp = Blueprint("save_ai_bp", __name__, url_prefix="/api")


@save_ai_bp.route("/save-ai", methods=["POST"])
def save_ai():

    # ----------------------------
    # 1. Validate JSON request
    # ----------------------------
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Invalid request format. JSON expected."
        }), 400

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "No data received."
        }), 400

    analysis_id = data.get("analysis_id")
    summary = data.get("summary", "")
    feedback = data.get("feedback", "")
    questions = data.get("questions", "")
    roadmap = data.get("roadmap", "")

    if not analysis_id:
        return jsonify({
            "success": False,
            "error": "Missing analysis_id."
        }), 400

    try:
        conn = sqlite3.connect("ats_data.db")
        cursor = conn.cursor()

        # ----------------------------
        # 2. Verify record exists
        # ----------------------------
        cursor.execute("SELECT id FROM analysis WHERE id=?", (analysis_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return jsonify({
                "success": False,
                "error": "Analysis record not found."
            }), 404

        # ----------------------------
        # 3. Save AI results
        # ----------------------------
        cursor.execute("""
        UPDATE analysis
        SET summary=?, feedback=?, questions=?, roadmap=?
        WHERE id=?
        """, (summary, feedback, questions, roadmap, analysis_id))

        conn.commit()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500