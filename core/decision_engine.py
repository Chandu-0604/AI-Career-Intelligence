def generate_decision(hire_score, matched_skills, missing_skills):
    """
    Convert scores into real recruiter decision
    """

    decision = {}
    matched_count = len(matched_skills)
    missing_count = len(missing_skills)

    # Determine Interview Decision
    if hire_score >= 70:
        decision_status = "INTERVIEW READY"
        decision_color = "green"
    elif hire_score >= 45:
        decision_status = "NEEDS IMPROVEMENT"
        decision_color = "orange"
    else:
        decision_status = "NOT INTERVIEW READY"
        decision_color = "red"

    # Determine Closest Role Fit
    if matched_count > missing_count:
        closest_role = "Backend / Software Developer"
    elif "machine learning" in [s.lower() for s in missing_skills]:
        closest_role = "General Software Developer (Not ML Ready)"
    else:
        closest_role = "Entry-Level Developer"

    # Main Gap Summary
    if missing_count > 0:
        main_gap = ", ".join(missing_skills[:3])
    else:
        main_gap = "No major skill gaps"

    decision["status"] = decision_status
    decision["color"] = decision_color
    decision["closest_role"] = closest_role
    decision["main_gap"] = main_gap

    return decision