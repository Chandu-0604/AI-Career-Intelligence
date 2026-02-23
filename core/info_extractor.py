import re

# ---------------- EMAIL ----------------
def extract_email(text):

    # remove hidden unicode spaces
    text = text.replace("\xa0", " ")

    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(email_pattern, text)

    if match:
        return match.group(0)

    return "Not Found"


# ---------------- PHONE ----------------
def extract_phone(text):

    # remove unicode spacing
    text = text.replace("\xa0", " ")

    # find all number groups (10 to 15 digits)
    possible_numbers = re.findall(r"\+?\d[\d\-\s()]{8,}\d", text)

    for num in possible_numbers:

        # remove all non digits
        digits = re.sub(r"\D", "", num)

        # Indian mobile handling
        if len(digits) == 12 and digits.startswith("91"):
            return digits[2:]   # remove country code

        if len(digits) == 11 and digits.startswith("0"):
            return digits[1:]

        if len(digits) >= 10:
            return digits[-10:]  # take last 10 digits

    return "Not Found"

# ---------------- NAME (SMART DETECTOR) ----------------
def extract_name(text):

    email = extract_email(text)
    phone = extract_phone(text)

    # choose anchor position in raw text
    anchor_pos = None

    if email != "Not Found":
        anchor_pos = text.find(email)

    elif phone != "Not Found":
        anchor_pos = text.find(phone)

    # If anchor found → look before it
    if anchor_pos and anchor_pos > 0:

        snippet = text[max(0, anchor_pos - 300):anchor_pos]

        lines = [l.strip() for l in snippet.split("\n") if l.strip()]

        # reverse search (closest line first)
        for line in reversed(lines):

            # skip long sentences
            if len(line) > 40:
                continue

            # skip digits
            if any(char.isdigit() for char in line):
                continue

            # skip common resume headings
            blacklist = [
                "summary", "objective", "profile",
                "experience", "education", "skills",
                "professional"
            ]

            if any(word in line.lower() for word in blacklist):
                continue

            words = line.split()

            if 2 <= len(words) <= 4:
                return line

    # fallback → first valid short line
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    for line in lines[:10]:
        if 2 <= len(line.split()) <= 4 and not any(char.isdigit() for char in line):
            return line

    return "Not Found"