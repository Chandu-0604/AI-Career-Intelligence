from core.skill_extractor import extract_skills
from core.job_parser import extract_job_skills
from ai.ai_skill_extractor import extract_ai_skills

# weight mapping
WEIGHTS = {
    "python":5,
    "machine learning":5,
    "deep learning":5,
    "tensorflow":5,
    "pytorch":5,
    "scikit-learn":5,

    "flask":4,
    "django":4,
    "fastapi":4,
    "rest api":4,
    "restful api":4,

    "pandas":3,
    "numpy":3,
    "data analysis":3,
    "matplotlib":3,
    "seaborn":3,

    "docker":2,
    "aws":2,
    "azure":2,
    "gcp":2,
    "kubernetes":2,

    "git":1,
    "github":1,
    "linux":1,
    "postman":1,
    "sql":2,
    "mysql":2,
    "mongodb":2
}


def skill_weight(skill):
    return WEIGHTS.get(skill, 1)


def calculate_ats_score(resume_text, job_description):

    # rule-based skills
    regex_skills = set(extract_skills(resume_text))

    # AI-based skills
    ai_skills = set(extract_ai_skills(resume_text))

    # combine both
    resume_skills = regex_skills.union(ai_skills)
    job_skills = set(extract_job_skills(job_description))

    if not job_skills:
        return 0, [], []

    matched = resume_skills.intersection(job_skills)
    missing = job_skills - resume_skills

    # weighted scoring
    total_weight = sum(skill_weight(s) for s in job_skills)
    matched_weight = sum(skill_weight(s) for s in matched)

    score = int((matched_weight / total_weight) * 100)

    return score, sorted(list(matched)), sorted(list(missing))