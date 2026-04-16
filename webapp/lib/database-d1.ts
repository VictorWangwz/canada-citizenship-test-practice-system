// D1 Database utility for Cloudflare Pages
// Replaces better-sqlite3 with D1 binding

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

export interface Env {
  DB: D1Database;
}

export async function getRandomQuestions(
  db: D1Database,
  count: number = 20
): Promise<QuestionWithOptions[]> {
  const { results } = await db
    .prepare(`SELECT * FROM questions ORDER BY RANDOM() LIMIT ?`)
    .bind(count)
    .all<Question>();
  
  // Parse options from JSON
  return (results || []).map(q => ({
    ...q,
    options: q.options ? JSON.parse(q.options) : []
  }));
}

export async function getQuestionById(
  db: D1Database,
  id: number
): Promise<QuestionWithOptions | null> {
  const question = await db
    .prepare(`SELECT * FROM questions WHERE id = ?`)
    .bind(id)
    .first<Question>();
  
  if (!question) return null;
  
  return {
    ...question,
    options: question.options ? JSON.parse(question.options) : []
  };
}

export async function getQuestionCount(db: D1Database): Promise<number> {
  const result = await db
    .prepare('SELECT COUNT(*) as count FROM questions')
    .first<{ count: number }>();
  
  return result?.count || 0;
}

export async function getStatistics(db: D1Database) {
  const total = await getQuestionCount(db);
  
  const { results: bySources } = await db
    .prepare(`
      SELECT source, COUNT(*) as count 
      FROM questions 
      WHERE source IS NOT NULL 
      GROUP BY source
    `)
    .all<{ source: string; count: number }>();
  
  return {
    total,
    by_source: bySources || []
  };
}
