import re

def clean_resume_text(text):

    if not text:
        return ""

    # Convert to uniform newlines
    text = text.replace("\r", "\n")

    # Remove multiple spaces
    text = re.sub(r'[ \t]+', ' ', text)

    # Remove repeated blank lines
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    # Fix spaced emails (common PDF issue)
    text = re.sub(r'\s*@\s*', '@', text)
    text = re.sub(r'\s*\.\s*', '.', text)

    # Fix phone numbers split by spaces
    text = re.sub(r'(\d)\s+(\d)', r'\1\2', text)

    # Remove bullet characters
    text = re.sub(r'[•●▪►]', ' ', text)

    # Remove weird unicode
    text = text.encode('ascii', 'ignore').decode()

    return text.strip()