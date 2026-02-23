import re

def parse_roadmap(roadmap_text):

    weeks = []
    current_week = None

    lines = roadmap_text.split("\n")

    for line in lines:
        line = line.strip()

        # detect week
        week_match = re.search(r"Week\s*(\d+)", line, re.IGNORECASE)
        if week_match:
            if current_week:
                weeks.append(current_week)

            current_week = {
                "title": line,
                "topics": [],
                "practice": [],
                "project": [],
                "outcome": []
            }
            continue

        if not current_week:
            continue

        # classify content
        lower = line.lower()

        if "topic:" in lower:
            current_week["topics"].append(line.split(":",1)[1].strip())

        elif "practice:" in lower:
            current_week["practice"].append(line.split(":",1)[1].strip())

        elif "mini task" in lower or "project" in lower:
            current_week["project"].append(line.split(":",1)[-1].strip())

        elif len(line) > 20:
            current_week["outcome"].append(line)

    if current_week:
        weeks.append(current_week)

    return weeks