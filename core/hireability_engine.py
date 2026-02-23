import re
from core.skill_extractor import extract_skills

# -----------------------------
# Skill categories
# -----------------------------

CORE_SKILLS = {
    "python","java","c++","machine learning","deep learning",
    "tensorflow","pytorch","scikit-learn","data analysis"
}

TOOLS = {
    "git","github","linux","docker","postman","kubernetes","aws","azure","gcp"
}

FRAMEWORKS = {
    "flask","django","fastapi","spring","react","nodejs","express"
}

DATABASES = {
    "mysql","postgresql","mongodb","sqlite","sql server"
}


# -----------------------------
# Project Complexity Detector
# -----------------------------

def project_complexity_score(resume_text):

    score = 0
    text = resume_text.lower()

    # backend indicators
    if "api" in text or "backend" in text:
        score += 15

    # database usage
    if "database" in text or "sql" in text:
        score += 15

    # authentication / security
    if "authentication" in text or "login" in text:
        score += 10

    # blockchain / advanced
    if "blockchain" in text or "smart contract" in text:
        score += 20

    # deployment / hosting
    if "deploy" in text or "cloud" in text:
        score += 20

    return min(score, 100)


# -----------------------------
# MAIN HIREABILITY SCORE
# -----------------------------

def calculate_hireability(resume_text, job_description):

    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    if not job_skills:
        return 0, {}

    # --------------------------
    # 1️⃣ Core Job Match
    # --------------------------
    core_match = len(resume_skills & job_skills) / len(job_skills) * 100

    # --------------------------
    # 2️⃣ Tooling Depth
    # --------------------------
    tool_depth = len(resume_skills & TOOLS) / max(len(TOOLS),1) * 100

    # --------------------------
    # 3️⃣ Framework Depth
    # --------------------------
    framework_depth = len(resume_skills & FRAMEWORKS) / max(len(FRAMEWORKS),1) * 100

    # --------------------------
    # 4️⃣ Project Strength
    # --------------------------
    experience = project_complexity_score(resume_text)

    # --------------------------
    # Weighted Score
    # --------------------------
    final_score = (
        0.50 * core_match +
        0.20 * tool_depth +
        0.10 * framework_depth +
        0.20 * experience
    )

    breakdown = {
        "core_job_match": round(core_match),
        "tool_depth": round(tool_depth),
        "framework_depth": round(framework_depth),
        "experience": round(experience)
    }

    return round(final_score), breakdown