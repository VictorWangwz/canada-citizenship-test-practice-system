// Results page showing score and explanations
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

interface QuestionResult {
  questionId: number;
  question: string;
  userAnswer: string;
  correctAnswer: string;
  isCorrect: boolean;
  explanation: string;
  category: string | null;
}

interface TestResults {
  success: boolean;
  results: QuestionResult[];
  summary: {
    totalQuestions: number;
    correctCount: number;
    incorrectCount: number;
    score: number;
    passed: boolean;
  };
}

export default function ResultsPage() {
  const router = useRouter();
  const [results, setResults] = useState<TestResults | null>(null);

  useEffect(() => {
    const storedResults = sessionStorage.getItem('testResults');
    if (storedResults) {
      setResults(JSON.parse(storedResults));
    } else {
      router.push('/');
    }
  }, [router]);

  if (!results) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-xl text-gray-600">Loading results...</div>
      </div>
    );
  }

  const { summary, results: questionResults } = results;

  return (
    <main className="min-h-screen bg-white">
      {/* Government of Canada Header */}
      <div className="border-b-4 border-red-600">
        <div className="bg-white px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-8">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-red-600 flex items-center justify-center">
                <span className="text-white text-2xl">🍁</span>
              </div>
              <div>
                <div className="text-sm font-semibold">Government</div>
                <div className="text-sm font-semibold">of Canada</div>
              </div>
            </div>
          </div>
          <div className="text-right text-sm">
            <div><span className="font-semibold">Application number:</span> M2222222222</div>
            <div><span className="font-semibold">UCI:</span> 1234567890</div>
          </div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-8 py-12">
        <h1 className="text-3xl font-bold mb-8">Test results</h1>

        {/* Score summary */}
        <div className={`border-l-4 p-8 mb-8 ${
          summary.passed ? 'bg-green-50 border-green-600' : 'bg-red-50 border-red-600'
        }`}>
          <div className="mb-6">
            <h2 className={`text-4xl font-bold mb-2 ${
              summary.passed ? 'text-green-800' : 'text-red-800'
            }`}>
              {summary.passed ? '✓ You passed!' : '✗ You did not pass'}
            </h2>
            <p className="text-2xl font-semibold mb-4">
              Your score: {summary.score}% ({summary.correctCount} out of {summary.totalQuestions} correct)
            </p>
          </div>
          
          <div className={`p-4 rounded ${
            summary.passed ? 'bg-green-100' : 'bg-red-100'
          }`}>
            <p className="text-lg">
              {summary.passed 
                ? 'You answered at least 16 out of 20 questions correctly. In the official test, this would be a passing score.'
                : 'You need to answer at least 16 out of 20 questions correctly (80%) to pass the citizenship test. Keep studying and try again!'}
            </p>
          </div>
        </div>

        {/* Statistics */}
        <div className="bg-gray-50 border border-gray-300 rounded p-6 mb-8">
          <h3 className="text-xl font-semibold mb-4">Test statistics</h3>
          <div className="grid grid-cols-3 gap-6">
            <div>
              <div className="text-3xl font-bold text-green-600">{summary.correctCount}</div>
              <div className="text-sm text-gray-600">Correct answers</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-red-600">{summary.incorrectCount}</div>
              <div className="text-sm text-gray-600">Incorrect answers</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600">{summary.totalQuestions}</div>
              <div className="text-sm text-gray-600">Total questions</div>
            </div>
          </div>
        </div>

        {/* Question review */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-6">Review your answers</h2>
          
          <div className="space-y-6">
            {questionResults.map((result, idx) => (
              <div
                key={result.questionId}
                className={`border-l-4 p-6 bg-white border ${
                  result.isCorrect ? 'border-green-500 bg-green-50' : 'border-red-500 bg-red-50'
                }`}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-sm font-semibold text-gray-600">
                        Question {idx + 1}
                      </span>
                      {result.category && (
                        <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                          {result.category}
                        </span>
                      )}
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">
                      {result.question}
                    </h3>
                  </div>
                  <div className={`flex-shrink-0 ml-4 px-4 py-2 rounded font-bold text-sm ${
                    result.isCorrect
                      ? 'bg-green-600 text-white'
                      : 'bg-red-600 text-white'
                  }`}>
                    {result.isCorrect ? '✓ Correct' : '✗ Incorrect'}
                  </div>
                </div>

                <div className="space-y-3">
                  <div className={`p-4 rounded border ${
                    result.isCorrect
                      ? 'bg-green-100 border-green-300'
                      : 'bg-red-100 border-red-300'
                  }`}>
                    <div className="font-semibold mb-1">Your answer:</div>
                    <div>{result.userAnswer || 'Not answered'}</div>
                  </div>

                  {!result.isCorrect && (
                    <div className="p-4 rounded border bg-green-100 border-green-300">
                      <div className="font-semibold mb-1">Correct answer:</div>
                      <div>{result.correctAnswer}</div>
                    </div>
                  )}

                  {result.explanation && (
                    <div className="p-4 rounded border bg-blue-50 border-blue-300">
                      <div className="font-semibold mb-1">Explanation:</div>
                      <div>{result.explanation}</div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Action buttons */}
        <div className="flex gap-4 justify-center">
          <button
            onClick={() => router.push('/')}
            className="px-8 py-3 rounded bg-blue-600 text-white font-semibold hover:bg-blue-700"
          >
            Take another practice test
          </button>
        </div>
      </div>
    </main>
  );
}
