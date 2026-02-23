from flask import Blueprint, jsonify
from database.database import get_analysis_by_id
from ai.ai_feedback import (
    generate_feedback,
    generate_summary,
    generate_interview_questions,
    generate_learning_roadmap
)
from ai.ai_response_parser import parse_ai_sections
import sqlite3
import json

ai_bp = Blueprint("ai_bp", __name__, url_prefix="/api")


@ai_bp.route("/ai-analysis/<int:analysis_id>", methods=["GET"])
def ai_analysis(analysis_id):

    record = get_analysis_by_id(analysis_id)

    if not record:
        return jsonify({"success": False, "error": "Analysis not found"}), 404

    resume_text = record["resume_text"]
    job_description = record["job_description"]
    missing_skills = record["missing_skills"].split(",") if record["missing_skills"] else []

    try:
        # ---------- AI GENERATION ----------
        feedback_raw = generate_feedback(resume_text, job_description)
        parsed = parse_ai_sections(feedback_raw)

        summary = generate_summary(resume_text)
        questions = generate_interview_questions(resume_text, job_description)
        roadmap = generate_learning_roadmap(resume_text, missing_skills)

        # ---------- SAVE DIRECTLY TO DB ----------
        conn = sqlite3.connect("ats_data.db")
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE analysis
        SET summary=?, feedback=?, questions=?, roadmap=?
        WHERE id=?
        """, (
            summary,
            json.dumps({
                "strengths": parsed["strengths"],
                "weaknesses": parsed["weaknesses"],
                "improvements": parsed["improvements"],
                "projects": parsed["projects"]
            }),
            questions,
            roadmap,
            analysis_id
        ))

        conn.commit()
        conn.close()

        # ---------- RESPONSE ----------
        return jsonify({
            "success": True,
            "summary": summary,
            "strengths": parsed["strengths"],
            "weaknesses": parsed["weaknesses"],
            "improvements": parsed["improvements"],
            "projects": parsed["projects"],
            "questions": questions,
            "roadmap": roadmap
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500