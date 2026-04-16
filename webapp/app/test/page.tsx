// Test interface with question display and navigation
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';

interface Question {
  id: number;
  question: string;
  type: string;
  options: string[];
  category: string | null;
  difficulty: string | null;
  explanation: string | null;
  source: string | null;
}

export default function TestPage() {
  const router = useRouter();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [markedForReview, setMarkedForReview] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeLeft, setTimeLeft] = useState(60 * 60); // 60 minutes in seconds
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  useEffect(() => {
    fetchQuestions();
  }, []);

  useEffect(() => {
    // Timer countdown
    if (timeLeft <= 0) return;
    
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timer);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const fetchQuestions = async () => {
    try {
      const response = await fetch('/api/questions?count=20');
      const data = await response.json();
      
      if (data.success) {
        setQuestions(data.questions);
      } else {
        setError(data.error || 'Failed to load questions');
      }
    } catch (err) {
      setError('Failed to connect to the server');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (optionIndex: number) => {
    const currentQuestion = questions[currentIndex];
    setAnswers({
      ...answers,
      [currentQuestion.id]: optionIndex
    });
  };

  const toggleReviewMark = () => {
    const currentQuestion = questions[currentIndex];
    const newMarked = new Set(markedForReview);
    if (newMarked.has(currentQuestion.id)) {
      newMarked.delete(currentQuestion.id);
    } else {
      newMarked.add(currentQuestion.id);
    }
    setMarkedForReview(newMarked);
  };

  const goToPrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const goToNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const submitTest = async () => {
    try {
      // Convert option indexes to letters for API
      const letterAnswers: Record<number, string> = {};
      Object.entries(answers).forEach(([qId, optionIdx]) => {
        letterAnswers[parseInt(qId)] = String.fromCharCode(65 + optionIdx); // 0->A, 1->B, etc.
      });

      const response = await fetch('/api/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ answers: letterAnswers }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Store results in sessionStorage and navigate to results page
        sessionStorage.setItem('testResults', JSON.stringify(data));
        router.push('/results');
      } else {
        setError(data.error || 'Failed to submit test');
      }
    } catch (err) {
      setError('Failed to submit test');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-xl text-gray-600">Loading questions...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-xl text-red-600">{error}</div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-xl text-gray-600">No questions available</div>
      </div>
    );
  }

  const currentQuestion = questions[currentIndex];
  const currentAnswer = answers[currentQuestion.id];
  const answeredCount = Object.keys(answers).filter(qId => !markedForReview.has(parseInt(qId))).length;
  const reviewCount = markedForReview.size;
  const notAnsweredCount = questions.length - Object.keys(answers).length;

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

      <div className="px-8 py-6">
        <h1 className="text-3xl font-bold mb-6">Online citizenship test</h1>
        
        <div className="flex gap-8">
          {/* Left side - Question */}
          <div className="flex-1">
            {/* Question number and timer */}
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Question {currentIndex + 1} of {questions.length}</h2>
              <div className="text-2xl font-bold">Time left {formatTime(timeLeft)}</div>
            </div>

            {/* Question text */}
            <div className="mb-6">
              <p className="text-xl font-semibold mb-6">{currentQuestion.question}</p>
              
              {/* Options as radio buttons */}
              <div className="space-y-4">
                {currentQuestion.options.map((option, idx) => {
                  const isSelected = currentAnswer === idx;
                  
                  return (
                    <label
                      key={idx}
                      className="flex items-start gap-3 cursor-pointer"
                    >
                      <input
                        type="radio"
                        name="answer"
                        checked={isSelected}
                        onChange={() => handleAnswerSelect(idx)}
                        className="mt-1 w-4 h-4"
                      />
                      <span className="text-base">{option}</span>
                    </label>
                  );
                })}
              </div>
            </div>

            {/* Mark for review checkbox */}
            <div className="mb-6">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={markedForReview.has(currentQuestion.id)}
                  onChange={toggleReviewMark}
                  className="w-4 h-4"
                />
                <span className="text-sm text-gray-700">I want to review this answer later.</span>
              </label>
            </div>

            {/* Navigation buttons */}
            <div className="flex gap-4 mb-6">
              <button
                onClick={goToPrevious}
                disabled={currentIndex === 0}
                className={`px-6 py-2 border rounded flex items-center gap-2 ${
                  currentIndex === 0
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed border-gray-300'
                    : 'bg-white text-gray-700 border-gray-400 hover:bg-gray-50'
                }`}
              >
                <span>←</span>
                <span>Previous question</span>
              </button>

              <button
                onClick={goToNext}
                disabled={currentIndex === questions.length - 1}
                className={`px-6 py-2 border rounded flex items-center gap-2 ${
                  currentIndex === questions.length - 1
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed border-gray-300'
                    : 'bg-white text-gray-700 border-gray-400 hover:bg-gray-50'
                }`}
              >
                <span>Next question</span>
                <span>→</span>
              </button>
            </div>

            {/* Confirm submission button */}
            <button
              onClick={submitTest}
              className="w-full bg-blue-600 text-white py-3 rounded font-semibold hover:bg-blue-700"
            >
              Confirm submission
            </button>
          </div>

          {/* Right side - Question navigator */}
          <div className="w-80 border-l pl-8">
            <div className="mb-4">
              <h3 className="text-lg font-bold mb-4">View questions</h3>
              
              {/* View mode toggle */}
              <div className="flex gap-2 mb-4">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`px-4 py-2 border rounded flex items-center gap-2 ${
                    viewMode === 'grid'
                      ? 'bg-gray-200 border-gray-400'
                      : 'bg-white border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <span>⊞</span>
                  <span>Grid view</span>
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`px-4 py-2 border rounded flex items-center gap-2 ${
                    viewMode === 'list'
                      ? 'bg-gray-200 border-gray-400'
                      : 'bg-white border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <span>☰</span>
                  <span>List view</span>
                </button>
              </div>
            </div>

            {/* Question navigator - Grid view */}
            {viewMode === 'grid' && (
              <div className="grid grid-cols-5 gap-2 mb-6">
                {questions.map((q, idx) => {
                  const isAnswered = answers[q.id] !== undefined;
                  const isReview = markedForReview.has(q.id);
                  const isCurrent = idx === currentIndex;
                  
                  let bgColor = 'bg-gray-300 text-gray-800'; // Not answered
                  if (isReview) {
                    bgColor = 'bg-orange-500 text-white'; // To be reviewed
                  } else if (isAnswered) {
                    bgColor = 'bg-blue-900 text-white'; // Answered
                  }
                  
                  if (isCurrent) {
                    bgColor += ' ring-2 ring-blue-500';
                  }
                  
                  return (
                    <button
                      key={q.id}
                      onClick={() => setCurrentIndex(idx)}
                      className={`w-12 h-12 rounded font-semibold text-sm ${bgColor} hover:opacity-80`}
                    >
                      {idx + 1}
                    </button>
                  );
                })}
              </div>
            )}

            {/* Question navigator - List view */}
            {viewMode === 'list' && (
              <div className="space-y-1 mb-6 max-h-96 overflow-y-auto">
                {questions.map((q, idx) => {
                  const isAnswered = answers[q.id] !== undefined;
                  const isReview = markedForReview.has(q.id);
                  const isCurrent = idx === currentIndex;
                  
                  let bgColor = 'bg-gray-100 text-gray-800'; // Not answered
                  let statusText = 'Not answered';
                  
                  if (isReview) {
                    bgColor = 'bg-orange-100 text-orange-900'; // To be reviewed
                    statusText = 'To be reviewed';
                  } else if (isAnswered) {
                    bgColor = 'bg-blue-100 text-blue-900'; // Answered
                    statusText = 'Answered';
                  }
                  
                  if (isCurrent) {
                    bgColor += ' ring-2 ring-blue-500';
                  }
                  
                  return (
                    <button
                      key={q.id}
                      onClick={() => setCurrentIndex(idx)}
                      className={`w-full text-left px-3 py-2 rounded text-sm ${bgColor} hover:opacity-80 flex justify-between items-center`}
                    >
                      <span className="font-semibold">Question {idx + 1}</span>
                      <span className="text-xs">{statusText}</span>
                    </button>
                  );
                })}
              </div>
            )}

            {/* Legend */}
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded bg-orange-500"></div>
                <span>To be reviewed: {reviewCount}</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded bg-gray-300"></div>
                <span>Not answered: {notAnsweredCount}</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 rounded bg-blue-900"></div>
                <span>Answered: {answeredCount}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
