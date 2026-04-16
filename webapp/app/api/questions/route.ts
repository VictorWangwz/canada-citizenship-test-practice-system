// API route to get random questions for a test
import { NextResponse } from 'next/server';
import { getRandomQuestions } from '@/lib/database-d1';
import { getRequestContext } from '@cloudflare/next-on-pages';

export const runtime = 'edge';

export async function GET(request: Request) {
  try {
    // Get D1 database binding from Cloudflare context
    const { env } = getRequestContext();
    const db = env.DB;
    
    const { searchParams } = new URL(request.url);
    const count = parseInt(searchParams.get('count') || '20', 10);
    
    const questions = await getRandomQuestions(db, count);
    
    // Remove correct_answer from response to prevent cheating
    const questionsWithoutAnswers = questions.map(({ correct_answer, ...rest }) => rest);
    
    return NextResponse.json({
      success: true,
      questions: questionsWithoutAnswers,
      count: questions.length
    });
  } catch (error) {
    console.error('Error fetching questions:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to fetch questions' },
      { status: 500 }
    );
  }
}
