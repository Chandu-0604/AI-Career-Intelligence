from groq import Groq
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_json_array(text):
    """
    Extracts JSON list from LLM response safely.
    """

    # remove code block markers
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE)

    # find first [ ... ] block
    match = re.search(r"\[.*?\]", text, re.DOTALL)

    if not match:
        return []

    json_text = match.group(0)

    try:
        return json.loads(json_text)
    except:
        return []


def extract_ai_skills(resume_text):

    prompt = f"""
You are an ATS resume parser.

Extract ONLY technical skills from this resume.

Rules:
- Only technologies, programming languages, frameworks, databases, tools
- No soft skills
- No explanations
- Return ONLY a JSON array

Example:
["python","flask","mysql","docker","aws"]

Resume:
{resume_text[:3000]}
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=300,
        )

        response = completion.choices[0].message.content.strip()

        skills = extract_json_array(response)

        return [s.lower().strip() for s in skills if len(s.strip()) > 1]

    except Exception as e:
        print("AI skill extraction failed:", e)
        return []