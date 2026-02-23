import re
import json

def extract_json(text):
    """
    Extract JSON object even if model wraps it in text or ```json blocks
    """

    # remove markdown code blocks
    text = text.strip()

    if "```" in text:
        text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

    # find first { and last }
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        return text[start:end+1]

    return None


def parse_ai_sections(text):

    sections = {
        "strengths": [],
        "weaknesses": [],
        "improvements": [],
        "projects": []
    }

    # ---------------------------
    # 1️⃣ TRY JSON PARSING FIRST
    # ---------------------------
    json_text = extract_json(text)

    if json_text:
        try:
            data = json.loads(json_text)

            for key in sections:
                if key in data and isinstance(data[key], list):
                    sections[key] = [str(x).strip() for x in data[key] if str(x).strip()]

            return sections
        except Exception:
            pass  # fallback to bullet parsing

    # ---------------------------
    # 2️⃣ FALLBACK: BULLET PARSER
    # ---------------------------
    current_section = None
    lines = text.split("\n")

    for line in lines:

        l = line.lower().strip()

        if "strength" in l:
            current_section = "strengths"
            continue
        elif "weakness" in l:
            current_section = "weaknesses"
            continue
        elif "improvement" in l or "recommendation" in l:
            current_section = "improvements"
            continue
        elif "project" in l:
            current_section = "projects"
            continue

        bullet_match = re.match(r'^\s*[-•*]\s+(.*)', line)
        if bullet_match and current_section:
            item = bullet_match.group(1).strip()
            if len(item) > 3:
                sections[current_section].append(item)

    return sections