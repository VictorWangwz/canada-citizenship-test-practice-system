"""SQLite database module for storing citizenship test questions."""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional
import config


class QuestionDatabase:
    """Manages the SQLite database for citizenship test questions."""
    
    def __init__(self, db_path: Path = None):
        """Initialize the database connection."""
        if db_path is None:
            db_path = config.DATA_DIR / "questions.db"
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the database schema if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create questions table
        cursor.execute("""
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
            )
        """)
        
        # Create index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_source 
            ON questions(source)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_category 
            ON questions(category)
        """)
        
        conn.commit()
        conn.close()
        print(f"Database initialized at {self.db_path}")
    
    def add_question(self, question: Dict) -> int:
        """
        Add a single question to the database.
        
        Args:
            question: Dictionary containing question data
            
        Returns:
            ID of the inserted question
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Serialize options list to JSON if it exists
        options = json.dumps(question.get('options', [])) if question.get('options') else None
        
        cursor.execute("""
            INSERT INTO questions 
            (question, type, options, correct_answer, category, difficulty, 
             explanation, source, chapter, question_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            question['question'],
            question.get('type', 'multiple_choice'),
            options,
            question['correct_answer'],
            question.get('category', 'General'),
            question.get('difficulty', 'medium'),
            question.get('explanation', ''),
            question.get('source', 'unknown'),
            question.get('chapter', ''),
            question.get('question_number', 0)
        ))
        
        question_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return question_id
    
    def add_questions_bulk(self, questions: List[Dict]) -> int:
        """
        Add multiple questions to the database.
        
        Args:
            questions: List of question dictionaries
            
        Returns:
            Number of questions added
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        count = 0
        for question in questions:
            options = json.dumps(question.get('options', [])) if question.get('options') else None
            
            cursor.execute("""
                INSERT INTO questions 
                (question, type, options, correct_answer, category, difficulty, 
                 explanation, source, chapter, question_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                question['question'],
                question.get('type', 'multiple_choice'),
                options,
                question['correct_answer'],
                question.get('category', 'General'),
                question.get('difficulty', 'medium'),
                question.get('explanation', ''),
                question.get('source', 'unknown'),
                question.get('chapter', ''),
                question.get('question_number', 0)
            ))
            count += 1
        
        conn.commit()
        conn.close()
        
        return count
    
    def get_random_questions(self, count: int = 20) -> List[Dict]:
        """
        Get random questions from the database.
        
        Args:
            count: Number of questions to retrieve
            
        Returns:
            List of question dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM questions 
            ORDER BY RANDOM() 
            LIMIT ?
        """, (count,))
        
        rows = cursor.fetchall()
        conn.close()
        
        questions = []
        for row in rows:
            question = dict(row)
            # Deserialize options from JSON
            if question['options']:
                question['options'] = json.loads(question['options'])
            questions.append(question)
        
        return questions
    
    def get_all_questions(self) -> List[Dict]:
        """Get all questions from the database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM questions ORDER BY id")
        rows = cursor.fetchall()
        conn.close()
        
        questions = []
        for row in rows:
            question = dict(row)
            if question['options']:
                question['options'] = json.loads(question['options'])
            questions.append(question)
        
        return questions
    
    def get_question_count(self) -> int:
        """Get total number of questions in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM questions")
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def get_questions_by_source(self, source: str) -> List[Dict]:
        """Get questions filtered by source."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM questions WHERE source = ?", (source,))
        rows = cursor.fetchall()
        conn.close()
        
        questions = []
        for row in rows:
            question = dict(row)
            if question['options']:
                question['options'] = json.loads(question['options'])
            questions.append(question)
        
        return questions
    
    def clear_database(self):
        """Clear all questions from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM questions")
        conn.commit()
        conn.close()
        
        print("Database cleared")
    
    def get_statistics(self) -> Dict:
        """Get database statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total questions
        cursor.execute("SELECT COUNT(*) FROM questions")
        total = cursor.fetchone()[0]
        
        # By source
        cursor.execute("""
            SELECT source, COUNT(*) as count 
            FROM questions 
            GROUP BY source
        """)
        by_source = {row[0]: row[1] for row in cursor.fetchall()}
        
        # By category
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM questions 
            GROUP BY category
        """)
        by_category = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total': total,
            'by_source': by_source,
            'by_category': by_category
        }


if __name__ == "__main__":
    # Test the database
    db = QuestionDatabase()
    
    # Test adding a question
    test_question = {
        'question': 'What is the capital of Canada?',
        'type': 'multiple_choice',
        'options': ['Toronto', 'Ottawa', 'Montreal', 'Vancouver'],
        'correct_answer': 'Ottawa',
        'category': 'Geography',
        'difficulty': 'easy',
        'explanation': 'Ottawa has been the capital of Canada since 1857.',
        'source': 'test'
    }
    
    qid = db.add_question(test_question)
    print(f"Added question with ID: {qid}")
    
    # Get statistics
    stats = db.get_statistics()
    print(f"\nDatabase statistics: {stats}")
    
    # Get random questions
    random_q = db.get_random_questions(1)
    print(f"\nRandom question: {random_q[0]['question']}")
