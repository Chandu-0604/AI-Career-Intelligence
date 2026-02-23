import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- FEEDBACK ----------------
def generate_feedback(resume_text, job_description):

    prompt = f"""
You are a STRICT ATS recruiter.

You MUST ONLY use information present in the resume.
DO NOT invent experience.
If resume shows student → treat as fresher.
If something is missing → say missing.

Return ONLY valid JSON.

Format EXACTLY:

{{
"strengths": ["point","point"],
"weaknesses": ["point","point"],
"improvements": ["action","action"],
"projects": ["project idea","project idea"]
}}

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text[:3500]}
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=900
    )

    return completion.choices[0].message.content


# ---------------- SUMMARY ----------------
def generate_summary(resume_text):

    prompt = f"""
Write a professional resume summary.

STRICT RULES:
- Candidate is a student or fresher unless resume clearly shows job experience
- DO NOT add fake years of experience
- Mention technologies only from resume
- 4 to 5 lines paragraph
- No HR recruiter role unless present in resume

Resume:
{resume_text[:2500]}
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3,
        max_tokens=300
    )

    return completion.choices[0].message.content


# ---------------- QUESTIONS ----------------
def generate_interview_questions(resume_text, job_description):

    prompt = f"""
Create realistic interview questions based ONLY on resume skills.

Return markdown format:

## Technical
- question
- question

## Project
- question
- question

## HR
- question
- question

Resume:
{resume_text[:2500]}

Job:
{job_description[:2000]}
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3,
        max_tokens=800
    )

    return completion.choices[0].message.content


# ---------------- ROADMAP ----------------
def generate_learning_roadmap(resume_text, missing_skills):

    missing = ", ".join(missing_skills[:8])

    prompt = f"""
Create a 6 week learning roadmap for a beginner student.

Rules:
- Beginner level
- No advanced enterprise tasks
- Clear weekly steps
- Bullet format

Missing Skills:
{missing}

Resume:
{resume_text[:2000]}
"""

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}],
        temperature=0.4,
        max_tokens=900
    )

    return completion.choices[0].message.content