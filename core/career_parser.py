def parse_career_analysis(text):

    result = {
        "career_fit": "",
        "confidence": "",
        "strength": "",
        "gap": "",
        "recommendation": ""
    }

    lines = text.split("\n")

    for line in lines:
        if "CAREER_FIT:" in line:
            result["career_fit"] = line.split(":",1)[1].strip()

        elif "CONFIDENCE:" in line:
            result["confidence"] = line.split(":",1)[1].strip()

        elif "STRENGTH:" in line:
            result["strength"] = line.split(":",1)[1].strip()

        elif "GAP:" in line:
            result["gap"] = line.split(":",1)[1].strip()

        elif "RECOMMENDATION:" in line:
            result["recommendation"] = line.split(":",1)[1].strip()

    return result