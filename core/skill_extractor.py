import json
import re

def normalize(text):
    text = text.lower()

    # Replace hyphenated words with space (machine-learning → machine learning)
    text = re.sub(r'[-/]', ' ', text)

    # Keep + and # for skills like c++ and c#
    text = re.sub(r'[^a-z0-9+#.\s]', ' ', text)

    return text


def flexible_skill_match(skill, text):
    """
    Matches:
    python → python, python3, python-based
    machine learning → machine-learning
    rest api → rest apis
    """

    skill = skill.lower()

    # allow optional plural s
    pattern = r'\b' + re.escape(skill) + r's?\b'

    return re.search(pattern, text)


def extract_skills(text):

    text = normalize(text)

    with open("skills_db.json", "r") as f:
        skills_db = json.load(f)

    found_skills = set()

    for category in skills_db:
        for skill in skills_db[category]:

            if flexible_skill_match(skill, text):
                found_skills.add(skill)

    return sorted(list(found_skills))