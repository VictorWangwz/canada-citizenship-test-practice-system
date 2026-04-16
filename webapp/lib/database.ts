// Database utility for accessing question database
import Database from 'better-sqlite3';
import path from 'path';

export interface Question {
  id: number;
  question: string;
  type: string;
  options: string | null;
  correct_answer: string;
  category: string | null;
  difficulty: string | null;
  explanation: string | null;
  source: string | null;
  chapter: string | null;
  question_number: number | null;
}

export interface QuestionWithOptions extends Omit<Question, 'options'> {
  options: string[];
}

// Support both local development and Docker environments
const DB_PATH = process.env.DB_PATH || path.join(process.cwd(), '..', 'data', 'questions.db');

export function getDatabase() {
  const db = new Database(DB_PATH, { readonly: true });
  return db;
}

export function getRandomQuestions(count: number = 20): QuestionWithOptions[] {
  const db = getDatabase();
  
  const questions = db.prepare(`
    SELECT * FROM questions 
    ORDER BY RANDOM() 
    LIMIT ?
  `).all(count) as Question[];
  
  db.close();
  
  // Parse options from JSON
  return questions.map(q => ({
    ...q,
    options: q.options ? JSON.parse(q.options) : []
  }));
}

export function getQuestionById(id: number): QuestionWithOptions | null {
  const db = getDatabase();
  
  const question = db.prepare(`
    SELECT * FROM questions WHERE id = ?
  `).get(id) as Question | undefined;
  
  db.close();
  
  if (!question) return null;
  
  return {
    ...question,
    options: question.options ? JSON.parse(question.options) : []
  };
}

export function getQuestionCount(): number {
  const db = getDatabase();
  const result = db.prepare('SELECT COUNT(*) as count FROM questions').get() as { count: number };
  db.close();
  return result.count;
}
