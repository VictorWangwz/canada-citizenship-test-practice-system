// API route to submit answers and get results
// Updated to use Cloudflare D1

import { NextRequest } from 'next/server';
import { getQuestionById } from '@/lib/database-d1';

export const runtime = 'edge';

interface SubmitRequestBody {
  answers: Record<string, string>;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json() as SubmitRequestBody;
    const { answers } = body; // answers: { questionId: userAnswer }
    
    if (!answers || typeof answers !== 'object') {
      return new Response(
        JSON.stringify({ success: false, error: 'Invalid request body' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }
    
    // @ts-ignore - D1 binding is available in Cloudflare Pages
    const db = request.env?.DB;
    
    if (!db) {
      return new Response(
        JSON.stringify({ success: false, error: 'Database not configured' }),
        { status: 500, headers: { 'Content-Type': 'application/json' } }
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
    
    return new Response(
      JSON.stringify({
        success: true,
        results,
        summary: {
          totalQuestions,
          correctCount,
          incorrectCount: totalQuestions - correctCount,
          score: Math.round(score),
          passed
        }
      }),
      { 
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  } catch (error) {
    console.error('Error submitting test:', error);
    return new Response(
      JSON.stringify({ success: false, error: 'Failed to submit test' }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
}
