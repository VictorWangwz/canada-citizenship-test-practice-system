# Canada Citizenship Test - Web Application

Interactive web application for practicing Canadian citizenship test questions.

## Quick Start

### 1. Populate the Database

First, you need to generate questions and save them to the database:

```powershell
# Navigate to project root
cd c:\Users\wangz\project\canada-citizenship-test

# Setup data sources (download PDF, extract YouTube content)
uv run python main.py --setup

# Generate questions from PDF using LLM
uv run python main.py --generate-llm --provider openai

# Check database statistics
uv run python main.py --stats
```

This should give you:
- ~211 questions from YouTube (extracted via pattern matching)
- ~100-200 questions from PDF (generated via LLM)

### 2. Install Dependencies

```powershell
# Navigate to webapp directory
cd webapp

# Install Node.js dependencies
npm install
```

### 3. Run the Development Server

```powershell
npm run dev
```

Open http://localhost:3000 in your browser.

## Features

### Home Page
- Welcome screen with test information
- "Start Test" button to begin

### Test Interface
- 20 randomly selected questions
- Multiple-choice format (A, B, C, D)
- Navigation buttons (Previous/Next)
- Progress bar showing current question
- Quick navigation grid to jump to any question
- Visual indicators for answered questions

### Results Page
- Final score percentage
- Pass/Fail indicator (80% threshold)
- Breakdown of correct/incorrect answers
- Detailed review of each question:
  - Your answer
  - Correct answer
  - Explanation
  - Category/topic

## Architecture

### Backend (Python)
- `database.py`: SQLite database management
- `data_extractor.py`: Extract content from YouTube and PDF
- `llm_question_generator.py`: Generate questions using OpenAI/Anthropic

### Frontend (Next.js)
- **App Router** structure (Next.js 14)
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **better-sqlite3** for database access

### API Routes
- `GET /api/questions?count=20`: Fetch random questions
- `POST /api/submit`: Submit answers and get graded results

### Database Schema
```sql
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    type TEXT NOT NULL,  -- 'multiple_choice'
    options TEXT,  -- JSON array of options
    correct_answer TEXT NOT NULL,
    category TEXT,
    difficulty TEXT,
    explanation TEXT,
    source TEXT,  -- 'youtube_transcript' or 'llm_generated'
    chapter TEXT,
    question_number INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Development

### File Structure
```
webapp/
├── app/
│   ├── page.tsx              # Home page
│   ├── layout.tsx            # Root layout
│   ├── globals.css           # Global styles (Tailwind)
│   ├── test/
│   │   └── page.tsx          # Test interface
│   ├── results/
│   │   └── page.tsx          # Results page
│   └── api/
│       ├── questions/
│       │   └── route.ts      # GET random questions
│       └── submit/
│           └── route.ts      # POST submit answers
├── lib/
│   └── database.ts           # Database utilities
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── next.config.js
```

### Adding New Features

1. **Add more question sources**: Modify `data_extractor.py`
2. **Change test length**: Update count in `/api/questions?count=20`
3. **Modify pass threshold**: Change `score >= 80` in `app/api/submit/route.ts`
4. **Customize styling**: Edit Tailwind classes in component files

## Production Build

```powershell
# Build for production
npm run build

# Start production server
npm start
```

## Troubleshooting

### "Failed to fetch questions"
- Ensure database exists: `c:\Users\wangz\project\canada-citizenship-test\data\questions.db`
- Check database has questions: `uv run python main.py --stats`
- Verify database path in `webapp/lib/database.ts`

### "npm install" fails
- Ensure Node.js 18+ is installed: `node --version`
- Try clearing npm cache: `npm cache clean --force`

### Database path errors
- The webapp looks for database at `../data/questions.db` (relative to webapp folder)
- Ensure you run `npm run dev` from the `webapp` directory

## API Documentation

### GET /api/questions

Fetch random questions for a test.

**Query Parameters:**
- `count` (optional): Number of questions (default: 20)

**Response:**
```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of Canada?",
      "type": "multiple_choice",
      "options": ["Toronto", "Ottawa", "Montreal", "Vancouver"],
      "category": "Geography",
      "difficulty": "easy"
      // Note: correct_answer is NOT included to prevent cheating
    }
  ],
  "count": 20
}
```

### POST /api/submit

Submit test answers and get results.

**Request Body:**
```json
{
  "answers": {
    "1": "B",
    "2": "A",
    "3": "C"
    // questionId: userAnswer
  }
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "questionId": 1,
      "question": "What is the capital of Canada?",
      "userAnswer": "B",
      "correctAnswer": "B",
      "isCorrect": true,
      "explanation": "Ottawa is the capital city of Canada.",
      "category": "Geography"
    }
  ],
  "summary": {
    "totalQuestions": 20,
    "correctCount": 16,
    "incorrectCount": 4,
    "score": 80,
    "passed": true
  }
}
```

## License

Educational use only.
