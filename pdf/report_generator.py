from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import uuid
import json

pdfmetrics.registerFont(TTFont("TNR", "static/Fonts/TIMES.TTF"))

# ------------------ STYLES ------------------

title = ParagraphStyle(name="Title", fontName="TNR", fontSize=26, spaceAfter=14)
section = ParagraphStyle(name="Section", fontName="TNR", fontSize=18, textColor=colors.HexColor("#1e3a8a"), spaceAfter=12)
normal = ParagraphStyle(name="Normal", fontName="TNR", fontSize=11, leading=16)
bullet = ParagraphStyle(name="Bullet", fontName="TNR", fontSize=11, leftIndent=14, leading=15)
small = ParagraphStyle(name="Small", fontName="TNR", fontSize=9, textColor=colors.grey)

# ------------------ MAIN ------------------

def generate_pdf_report(filename, data):

    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=60, bottomMargin=50)
    story = []

    # ================= EXECUTIVE PAGE =================

    report_id = str(uuid.uuid4())[:8].upper()
    today = datetime.now().strftime("%d %B %Y")

    decision = data["decision"]["status"]
    role = data["decision"]["closest_role"]
    gap = data["decision"]["main_gap"]

    decision_color = {
        "INTERVIEW READY": "#16a34a",
        "NEEDS IMPROVEMENT": "#f59e0b",
        "NOT INTERVIEW READY": "#dc2626"
    }.get(decision, "#2563eb")

    story.append(Paragraph("AI Career Intelligence", title))
    story.append(Paragraph("Executive Hiring Assessment", normal))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"Report ID: <b>{report_id}</b>", small))
    story.append(Paragraph(f"Generated: <b>{today}</b>", small))
    story.append(Spacer(1, 25))

    # Decision Banner
    decision_box = Table([[decision]], colWidths=[450], rowHeights=[70])
    decision_box.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor(decision_color)),
        ("TEXTCOLOR", (0,0), (-1,-1), colors.white),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONTNAME", (0,0), (-1,-1), "TNR"),
        ("FONTSIZE", (0,0), (-1,-1), 22)
    ]))
    story.append(decision_box)
    story.append(Spacer(1, 20))

    # Key Insights Panel
    insights = Table([
        ["Closest Suitable Role", role],
        ["Primary Skill Gap", gap],
        ["Technical Match Score", f"{data['score']}%"]
    ], colWidths=[200, 250])

    insights.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#eef2ff")),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("FONTNAME", (0,0), (-1,-1), "TNR"),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6)
    ]))

    story.append(insights)
    story.append(Spacer(1, 20))

    story.append(Paragraph(
        "This report evaluates the candidate's readiness for technical interviews using resume intelligence, skill alignment analysis, and recruiter-style evaluation.",
        normal
    ))

    story.append(PageBreak())

    # ================= CANDIDATE INFO =================

    story.append(Paragraph("Candidate Profile", section))

    info = Table([
        ["Name", data["name"]],
        ["Email", data["email"]],
        ["Phone", data["phone"]],
    ], colWidths=[150, 290])

    info.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#eef2ff")),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("FONTNAME", (0,0), (-1,-1), "TNR"),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6)
    ]))

    story.append(info)
    story.append(PageBreak())

    # ================= SKILLS =================

    story.append(Paragraph("Skill Gap Analysis", section))

    matched = data["matched"]
    missing = data["missing"]

    story.append(Paragraph("<b>Matched Skills</b>", normal))
    for s in matched:
        story.append(Paragraph(f"• {s}", bullet))

    story.append(Spacer(1, 18))

    story.append(Paragraph("<b>Missing Skills</b>", normal))
    for s in missing:
        story.append(Paragraph(f"• {s}", bullet))

    story.append(PageBreak())

    # ================= RECRUITER FEEDBACK =================

    story.append(Paragraph("Recruiter Evaluation", section))

    feedback = data.get("feedback_data", {})

    def add_block(title, items, color):
        if not items:
            return
        header = Table([[title]], colWidths=[450])
        header.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor(color)),
            ("TEXTCOLOR", (0,0), (-1,-1), colors.white),
            ("FONTNAME", (0,0), (-1,-1), "TNR"),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6)
        ]))
        story.append(header)
        story.append(Spacer(1, 8))
        for item in items:
            story.append(Paragraph(f"• {item}", bullet))
        story.append(Spacer(1, 14))

    add_block("Strengths", feedback.get("strengths", []), "#16a34a")
    add_block("Weaknesses", feedback.get("weaknesses", []), "#dc2626")
    add_block("Improvement Actions", feedback.get("improvements", []), "#f59e0b")
    add_block("Recommended Projects", feedback.get("projects", []), "#2563eb")

    story.append(PageBreak())

    # ================= SUMMARY =================

    story.append(Paragraph("Recommended Resume Summary", section))
    story.append(Spacer(1, 10))
    story.append(Paragraph(data.get("summary", ""), normal))
    story.append(PageBreak())

    # ================= QUESTIONS =================

    story.append(Paragraph("Predicted Interview Questions", section))
    questions_raw = data.get("questions", "")

    lines = questions_raw.split("\n")
    qno = 1

    for line in lines:

        line = line.strip()

        # Detect section headers (## Technical etc.)
        if line.startswith("##"):
            section_title = line.replace("##", "").strip()
            story.append(Spacer(1, 12))
            story.append(Paragraph(f"<b>{section_title}</b>", section))
            story.append(Spacer(1, 8))
            continue

        # Detect bullet questions
        if line.startswith("-"):
            question = line[1:].strip()
            story.append(Paragraph(f"{qno}. {question}", normal))
            story.append(Spacer(1, 6))
            qno += 1

    doc.build(story)