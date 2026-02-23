# 🚀 AI Career Intelligence Platform
### AI-Powered Resume Analyzer & Interview Readiness Dashboard

---

## 📌 Repository Description (Paste in GitHub “About” Section)

AI-powered resume analyzer that evaluates interview readiness, detects skill gaps using ATS-style matching, generates recruiter feedback with LLM integration, and produces a professional downloadable hiring report.

---

# 🧠 Project Overview

AI Career Intelligence is a full-stack Flask application that analyzes resumes against job descriptions and provides:

- ATS Match Score
- Interview Readiness Score
- Skill Gap Analysis
- Recruiter-Style Feedback
- AI-Generated Interview Questions
- 6-Week Learning Roadmap
- Professional Resume Summary
- Downloadable PDF Hiring Report
- History Tracking of Analyses

The system simulates a real recruiter evaluation workflow.

---

# ⚙️ Features

## 📄 Resume Processing
- Supports PDF and DOCX
- Extracts skills, education, projects, experience

## 📊 ATS & Skill Matching
- Keyword-based ATS scoring engine
- Skill gap detection
- Matched vs Missing visualization
- Role alignment percentage

## 🎯 Interview Readiness Engine
- Hireability score calculation
- Categorized decision:
  - Interview Ready
  - Needs Improvement
  - Not Interview Ready
- Main skill gap detection

## 🤖 AI Integration (Groq LLM)
- Recruiter feedback:
  - Strengths
  - Weaknesses
  - Improvements
  - Project suggestions
- Interview question generation
- Learning roadmap generation
- Resume summary generation

## 📈 Dashboard
- Interview readiness gauge
- Skill coverage chart
- Tab-based UI (Interview / Roadmap / Summary)
- Premium glass gradient design

## 📑 PDF Report
- Hiring decision panel
- Skill gap breakdown
- Recruiter evaluation
- Resume summary
- Learning roadmap
- Interview questions

---

# 🏗️ Project Structure

```
AI-Career-Intelligence/
│
├── ai/                # AI modules
├── core/              # ATS, skill extraction, decision engine
├── database/          # SQLite logic
├── pdf/               # PDF report generator
├── templates/         # HTML dashboard
├── static/            # CSS and assets
├── uploads/           # Temporary resume storage
├── app.py             # Main Flask app
├── requirements.txt
└── README.md
```

---

# 🛠 Tech Stack

Backend:
- Python 3
- Flask
- SQLite

Resume Parsing:
- pdfplumber
- python-docx
- docx2txt
- pytesseract (OCR fallback)

AI:
- Groq LLM API

Frontend:
- HTML
- CSS
- Bootstrap
- Chart.js

PDF:
- ReportLab

---

# 🚀 Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Chandu-0604/AI-Career-Intelligence.git
cd AI-Career-Intelligence
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

(Mac/Linux)
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Add Environment Variable

Create `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

## 5️⃣ Run Application

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

# 📌 Usage

1. Upload resume (PDF/DOCX)
2. Paste job description
3. Click Analyze
4. View:
   - ATS score
   - Interview readiness
   - Skill gap
   - AI feedback
5. Download full PDF report

---

# 🎓 Use Case

- Students preparing for placements
- Freshers checking skill alignment
- Professionals evaluating job readiness
- Demonstration of full-stack + AI integration skills

---

# 👨‍💻 Author

Chandan B  
Computer Science Undergraduate  
Bengaluru, India  

GitHub: https://github.com/Chandu-0604  
LinkedIn: https://linkedin.com/in/chandan-b-2950a626a  

---

⭐ If you find this useful, give the repository a star.
