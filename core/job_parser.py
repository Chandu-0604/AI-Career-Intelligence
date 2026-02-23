import json
import re

def extract_job_skills(job_description):

    if not job_description:
        return []

    # normalize text
    text = job_description.lower()
    text = re.sub(r'[-/]', ' ', text)
    text = re.sub(r'[^a-z0-9+#.\s]', ' ', text)

    # load skill database
    with open("skills_db.json", "r") as f:
        skills_db = json.load(f)

    found_skills = set()

    # search skills directly inside job description
    for category in skills_db:
        for skill in skills_db[category]:
            pattern = r'\b' + re.escape(skill) + r's?\b'
            if re.search(pattern, text):
                found_skills.add(skill)

    return sorted(list(found_skills))