import sqlite3

DB_NAME = "ats_data.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            score INTEGER,
            matched_skills TEXT,
            missing_skills TEXT,
            summary TEXT,
            feedback TEXT,
            resume_text TEXT,
            job_description TEXT
        )
        """)

    conn.commit()
    conn.close()


def save_analysis(name, email, phone, score, matched, missing, summary, feedback, resume_text, job_description):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analysis 
        (name, email, phone, score, matched_skills, missing_skills, summary, feedback, resume_text, job_description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name or "Not Found",
        email or "Not Found",
        phone or "Not Found",
        score,
        ", ".join(matched),
        ", ".join(missing),
        summary,
        feedback,
        resume_text,
        job_description
    ))

    conn.commit()
    analysis_id = cursor.lastrowid
    conn.close()

    return analysis_id


def get_analyses(page=1, per_page=10):
    offset = (page - 1) * per_page

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, phone, score
        FROM analysis
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (per_page, offset))

    rows = cursor.fetchall()
    conn.close()

    return rows

def get_analysis_by_id(analysis_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM analysis
        WHERE id = ?
    """, (analysis_id,))

    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None