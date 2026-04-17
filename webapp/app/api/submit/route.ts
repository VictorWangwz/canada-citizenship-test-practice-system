// API route to submit answers and get results
import { NextResponse } from 'next/server';
import { getQuestionById } from '@/lib/database-d1';
import { getRequestContext } from '@cloudflare/next-on-pages';

export const runtime = 'edge';

interface SubmitRequestBody {
  answers: Record<string, string>;
}

export async function POST(request: Request) {
  try {
    // Get D1 database binding from Cloudflare context
    const { env } = getRequestContext();
    const db = env.DB;
    
    const body = await request.json() as SubmitRequestBody;
    const { answers } = body; // answers: { questionId: userAnswer }
    
    if (!answers || typeof answers !== 'object') {
      return NextResponse.json(
        { success: false, error: 'Invalid request body' },
        { status: 400 }
      );
    }
    
    const results = [];
    let correctCount = 0;
    
    for (const [questionId, userAnswer] of Object.entries(answers)) {
      const question = await getQuestionById(db, parseInt(questionId));
      
      if (!question) {
        continue;
      }
      
      const isCorrect = question.correct_answer === userAnswer;
      if (isCorrect) correctCount++;
      
      results.push({
        questionId: question.id,
        question: question.question,
        userAnswer,
        correctAnswer: question.correct_answer,
        isCorrect,
        explanation: question.explanation || '',
        category: question.category
      });
    }
    
    const totalQuestions = results.length;
    const score = totalQuestions > 0 ? (correctCount / totalQuestions) * 100 : 0;
    const passed = score >= 80;
    
    return NextResponse.json({
      success: true,
      results,
      summary: {
        totalQuestions,
        correctCount,
        incorrectCount: totalQuestions - correctCount,
        score: Math.round(score),
        passed
      }
    });
  } catch (error) {
    console.error('Error submitting test:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to submit test' },
      { status: 500 }
    );
  }
}
