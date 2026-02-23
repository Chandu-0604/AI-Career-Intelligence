import re

def clean_markdown(text):
    if not text:
        return ""

    # remove markdown symbols
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'__', '', text)
    text = re.sub(r'`', '', text)
    text = re.sub(r'#+\s*', '', text)

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def split_into_bullets(text):
    if not text:
        return []

    # split sentences into readable bullet points
    parts = re.split(r'[.\n]', text)

    clean_parts = []
    for p in parts:
        p = p.strip()
        if len(p) > 4:
            clean_parts.append(p)

    return clean_parts