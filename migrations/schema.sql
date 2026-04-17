-- Schema for Cloudflare D1 Database
-- This creates the questions table structure

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    type TEXT NOT NULL,
    options TEXT,
    correct_answer TEXT NOT NULL,
    category TEXT,
    difficulty TEXT,
    explanation TEXT,
    source TEXT,
    chapter TEXT,
    question_number INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_source ON questions(source);
CREATE INDEX IF NOT EXISTS idx_category ON questions(category);
