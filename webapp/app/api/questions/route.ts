// API route to get random questions for a test
import { NextResponse } from 'next/server';
import { getRandomQuestions } from '@/lib/database';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const count = parseInt(searchParams.get('count') || '20', 10);
    
    const questions = getRandomQuestions(count);
    
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
