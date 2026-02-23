import os
import sys
import uuid
import json
from flask import Flask, redirect, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename
from core.decision_engine import generate_decision

# allow package imports when running directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# SAFE ENGINE
from core.analysis_engine import run_basic_analysis

# DATABASE
from database.database import get_analyses, get_analysis_by_id, init_db, save_analysis

# PDF
from pdf.report_generator import generate_pdf_report

# -----------------------------------
# Flask App Init
# -----------------------------------
app = Flask(__name__)

# Initialize database ONCE at startup
init_db()

# -----------------------------------
# Blueprints
# -----------------------------------
from ai.ai_routes import ai_bp
app.register_blueprint(ai_bp)

from ai.ai_save_routes import save_ai_bp
app.register_blueprint(save_ai_bp)

# -----------------------------------
# Upload configuration
# -----------------------------------
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -----------------------------------
# Helper: allowed file
# -----------------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# -----------------------------------
# Home Route
# -----------------------------------
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        if "resume" not in request.files:
            return render_template("index.html", error="No file uploaded.", analyzed=False)

        file = request.files["resume"]
        job_description = request.form.get("job_description", "")

        if file.filename == "":
            return render_template("index.html", error="Please select a resume file.", analyzed=False)

        if not allowed_file(file.filename):
            return render_template("index.html", error="Only PDF or DOCX allowed.", analyzed=False)

        # Save file
        filename = secure_filename(file.filename)
        unique_name = str(uuid.uuid4()) + "_" + filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
        file.save(filepath)

        # Run Basic Analysis
        analysis = run_basic_analysis(filepath, job_description)

        if not analysis["success"]:
            return render_template("index.html", error=analysis["error"], analyzed=False)

        data = analysis["data"]

        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        score = data["score"]
        matched = data["matched_skills"]
        missing = data["missing_skills"]
        hire_score = data["hire_score"]
        score_breakdown = data["score_breakdown"]
        decision = data["decision"]
        resume_text = data["resume_text"]

        # Hire Status
        if hire_score < 40:
            hire_status = "Not Ready"
            hire_color = "red"
        elif hire_score < 65:
            hire_status = "Consider"
            hire_color = "orange"
        else:
            hire_status = "Strong Candidate"
            hire_color = "green"

        # Save initial record (AI fields empty)
        analysis_id = save_analysis(
            name,
            email,
            phone,
            score,
            matched,
            missing,
            "",
            "",
            resume_text,
            job_description
        )

        return redirect(url_for("load_analysis", analysis_id=analysis_id))

    return render_template("index.html", analyzed=False)

# -----------------------------------
# History Page
# -----------------------------------
@app.route("/history")
def history():
    page = request.args.get("page", 1, type=int)
    analyses = get_analyses(page=page, per_page=10)
    return render_template("history.html", analyses=analyses, page=page)

@app.route("/analysis/<int:analysis_id>")
def load_analysis(analysis_id):

    record = get_analysis_by_id(analysis_id)
    if not record:
        return "Analysis not found"

    matched = record["matched_skills"].split(",") if record["matched_skills"] else []
    missing = record["missing_skills"].split(",") if record["missing_skills"] else []

    from core.decision_engine import generate_decision
    decision = generate_decision(int(record["score"]), matched, missing)

    return render_template(
        "index.html",
        analyzed=True,
        name=record["name"],
        email=record["email"],
        phone=record["phone"],
        score=record["score"],
        matched=matched,
        missing=missing,
        hire_score=record["score"],
        decision=decision,
        analysis_id=analysis_id
    )

# -----------------------------------
# Download PDF
# -----------------------------------
@app.route("/download_report/<int:analysis_id>")
def download_report(analysis_id):

    import sqlite3
    import json

    conn = sqlite3.connect("ats_data.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, email, phone, score,
               matched_skills, missing_skills,
               summary, feedback, questions, roadmap
        FROM analysis WHERE id=?
    """, (analysis_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return "Report not found"

    # IMPORTANT: Wait for AI to exist
    if not row[6] or not row[7]:
        return """
        <h2 style='font-family:Arial'>
        AI analysis still generating...<br><br>
        Please wait 6–10 seconds and try again.
        </h2>
        """

    try:
        feedback_data = json.loads(row[7]) if row[7] else {}
    except:
        feedback_data = {}

    data = {
        "name": row[0],
        "email": row[1],
        "phone": row[2],
        "score": row[3],
        "matched": row[4].split(",") if row[4] else [],
        "missing": row[5].split(",") if row[5] else [],
        "summary": row[6],
        "feedback_data": feedback_data,
        "questions": row[8],
        "roadmap": row[9],
        "decision": {
            "status": "INTERVIEW READY" if row[3] >= 70 else "NEEDS IMPROVEMENT" if row[3] >= 40 else "NOT INTERVIEW READY",
            "closest_role": "Software Developer",
            "main_gap": (row[5].split(",")[0] if row[5] else "Project Experience")
        }
    }

    from datetime import datetime
    safe_name = row[0].replace(" ", "_")
    date = datetime.now().strftime("%d-%m-%Y")

    filename = f"{safe_name}_AI_Report_{date}.pdf"
    generate_pdf_report(filename, data)

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)