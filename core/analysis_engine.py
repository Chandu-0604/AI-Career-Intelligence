from core.resume_parser import extract_resume_text
from core.info_extractor import extract_email, extract_phone, extract_name
from core.skill_extractor import extract_skills
from core.ats_matcher import calculate_ats_score
from core.hireability_engine import calculate_hireability
from core.decision_engine import generate_decision

def run_basic_analysis(filepath, job_description):
    """
    SAFE ANALYSIS ONLY
    No AI here
    """

    result = {
        "success": False,
        "error": None,
        "data": {}
    }

    try:
        # Resume text
        resume_text = extract_resume_text(filepath)
        if not resume_text:
            result["error"] = "Unable to read resume."
            return result

        # Candidate info
        name = extract_name(resume_text)
        email = extract_email(resume_text)
        phone = extract_phone(resume_text)

        # Skills + ATS
        score, matched_skills, missing_skills = calculate_ats_score(resume_text, job_description)

        # Hireability
        hire_score, score_breakdown = calculate_hireability(resume_text, job_description)

        # Generate recruiter decision
        decision = generate_decision(hire_score, matched_skills, missing_skills)

        result["success"] = True
        result["data"] = {
            "resume_text": resume_text,
            "name": name,
            "email": email,
            "phone": phone,
            "score": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "hire_score": hire_score,
            "score_breakdown": score_breakdown,
            "decision": decision
        }

        return result

    except Exception as e:
        result["error"] = str(e)
        return result