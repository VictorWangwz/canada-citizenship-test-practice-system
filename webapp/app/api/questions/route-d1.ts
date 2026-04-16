// API route to get random questions for a test
// Updated to use Cloudflare D1

import { NextRequest } from 'next/server';
import { getRandomQuestions } from '@/lib/database-d1';

export const runtime = 'edge';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const count = parseInt(searchParams.get('count') || '20', 10);
    
    // @ts-ignore - D1 binding is available in Cloudflare Pages
    const db = request.env?.DB;
    
    if (!db) {
      return new Response(
        JSON.stringify({ success: false, error: 'Database not configured' }),
        { status: 500, headers: { 'Content-Type': 'application/json' } }
      );
    }
    
    const questions = await getRandomQuestions(db, count);
    
    // Remove correct_answer from response to prevent cheating
    const questionsWithoutAnswers = questions.map(({ correct_answer, ...rest }) => rest);
    
    return new Response(
      JSON.stringify({
        success: true,
        questions: questionsWithoutAnswers,
        count: questions.length
      }),
      { 
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  } catch (error) {
    console.error('Error fetching questions:', error);
    return new Response(
      JSON.stringify({ success: false, error: 'Failed to fetch questions' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}
