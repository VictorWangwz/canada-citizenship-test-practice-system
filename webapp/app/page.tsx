// Home page with Start Test button
'use client';

import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  const startTest = () => {
    router.push('/test');
  };

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

      <div className="max-w-4xl mx-auto px-8 py-12">
        <h1 className="text-3xl font-bold mb-8">Online citizenship test - Practice Mode</h1>
        
        <div className="bg-blue-50 border-l-4 border-blue-600 p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">About this test</h2>
          <p className="text-gray-700 mb-4">
            This practice test will help you prepare for the official Canadian citizenship test. 
            You will be presented with 20 randomly selected questions covering Canadian history, 
            geography, government, laws, and symbols.
          </p>
          <p className="text-gray-700">
            <strong>To pass the official test, you must answer at least 16 out of 20 questions correctly (80%).</strong>
          </p>
        </div>

        <div className="bg-white border border-gray-300 rounded p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">What to expect:</h2>
          <ul className="space-y-3 text-gray-700">
            <li className="flex items-start">
              <span className="mr-3 text-green-600">✓</span>
              <span>20 multiple-choice questions</span>
            </li>
            <li className="flex items-start">
              <span className="mr-3 text-green-600">✓</span>
              <span>60 minutes to complete the test</span>
            </li>
            <li className="flex items-start">
              <span className="mr-3 text-green-600">✓</span>
              <span>Navigate between questions and change your answers</span>
            </li>
            <li className="flex items-start">
              <span className="mr-3 text-green-600">✓</span>
              <span>Mark questions for review</span>
            </li>
            <li className="flex items-start">
              <span className="mr-3 text-green-600">✓</span>
              <span>Immediate results with detailed explanations</span>
            </li>
          </ul>
        </div>

        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 mb-8">
          <h3 className="font-semibold mb-2">⚠️ Important notes:</h3>
          <ul className="space-y-2 text-gray-700 text-sm">
            <li>• This is a practice test for educational purposes only</li>
            <li>• Questions are randomly selected from the official study guide</li>
            <li>• Your progress is not saved if you close this window</li>
          </ul>
        </div>
        
        <button
          onClick={startTest}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-8 rounded text-lg transition-colors"
        >
          Start Practice Test
        </button>
      </div>
    </main>
  );
}
