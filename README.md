# Canada Citizenship Test Generator

Automated system for generating randomized practice tests for the Canadian citizenship exam. Extracts content from official sources and creates customizable mock tests.

## 📋 Overview

This system:
- ✅ Extracts content from YouTube videos using pattern matching (no LLM)
- ✅ Downloads and parses the official "Discover Canada" PDF guide
- ✅ Uses AI (OpenAI GPT or Anthropic Claude) to generate high-quality questions from PDF
- ✅ Stores all questions in SQLite database
- ✅ **Interactive web application** with Next.js for test practice
- ✅ Random selection of 20 questions per test
- ✅ Navigate between questions freely and change answers
- ✅ Automatic grading with 80% pass threshold
- ✅ Detailed explanations for all questions

## 🆕 What's New

**Web Application:**
- Interactive Next.js web interface for test practice
- Random 20-question selection from database
- Navigate between questions (previous/next buttons)
- Change answers before submitting
- Automatic grading with pass/fail (80% threshold)
- Detailed results page with explanations
- Modern, responsive UI with Tailwind CSS

**Intelligent Question Generation:**
- Pattern matching for YouTube quiz format extraction (no LLM needed)
- LLM-powered question generation from PDF content only
- SQLite database for persistent question storage
- Multiple questions per PDF chapter with varying difficulty levels
- Creates realistic distractors for multiple-choice questions
- Includes explanations for correct answers

## 🎯 Features

- **Advanced Data Extraction**: Automatically extracts content from:
  - YouTube videos: Subtitles, auto-captions, or video description
  - Official PDF: https://www.canada.ca/content/dam/ircc/migration/ircc/english/pdf/pub/discover-large.pdf
  - Chapter detection and organization from PDF

- **AI-Powered Question Generation**: 
  - Uses GPT-4 (OpenAI) or Claude (Anthropic) to generate questions
  - Generates multiple questions per chapter
  - Varies difficulty levels (easy, medium, hard)
  - Creates realistic multiple-choice distractors
  - Includes explanations for answers

- **Flexible Question Database**: 
  - Pre-loaded with 25+ sample questions
  - LLM-generated questions from official PDF content
  - Questions covering: Geography, Government & Politics, History, Culture & Symbols, Rights & Responsibilities

- **Smart Test Generation**: Creates unique tests each time with randomized:
  - Question selection
  - Multiple choice option order
  
- **Interactive & CLI Modes**: Choose your preferred workflow
- **Answer Keys with Explanations**: Self-checking with detailed explanations

## 🚀 Quick Start

### 1. Install uv (if not already installed)

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

### 2. Install Dependencies

The project uses [uv](https://docs.astral.sh/uv/) for fast, reliable package management.

```powershell
uv sync
```

This will create a virtual environment and install all dependencies automatically.

### 3. Setup API Keys for LLM Question Generation

To use AI-powered question generation, you need an API key from OpenAI or Anthropic:

```powershell
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key:
# - For OpenAI: Get key from https://platform.openai.com/api-keys
# - For Anthropic: Get key from https://console.anthropic.com/
```

**Option A: Web Application (Recommended)**

```powershell
# First, populate the database with questions
uv run python main.py --setup
uv run python main.py --generate-llm --provider openai

# Then start the web server
cd webapp
npm install
npm run dev
```

Open http://localhost:3000 in your browser to start practicing!

**Option B: Docker Deployment (Easy Setup)**

```powershell
# First, populate the database with questions (run on host machine)
uv run python main.py --setup
uv run python main.py --generate-llm --provider openai

# Then use the Docker setup script
.\docker-setup.ps1

# Or manually with docker-compose
docker-compose up --build
```

Open http://localhost:3000 in your browser. See [webapp/DOCKER.md](webapp/DOCKER.md) for detailed Docker instructions.

**Option C: Command-Line Interfaceion generation is optional. You can still use the pre-loaded sample questions without API keys.

### 4. Run the Application

**Interactive Mode:**
```powershell
uv run python main.py
```

**Generate Questions with LLM (recommended):**
```powershell
# First, setup data sources (download PDF, extract content)
uv run python main.py --setup

# Then generate questions using OpenAI
uv run python main.py --generate-llm --provider openai

# Or use Anthropic Claude
uv run python main.py --generate-llm --provider anthropic
```

**Command-Line Options:**
```powershell (CLI)
├── data_extractor.py            # YouTube & PDF extraction logic
├── test_generator.py            # Test generation engine
├── llm_question_generator.py   # LLM-powered question generator
├── database.py                  # SQLite database management
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies (legacy)
├── pyproject.toml               # Modern dependency management (uv)
├── .env.example                 # Example environment variables
├── .env                         # Your API keys (create from .env.example)
├── README.md                    # This file
├── PLAN.md                      # Development plan
├── webapp/                      # Next.js web application
│   ├── app/                     # App router pages and layouts
│   │   ├── page.tsx             # Home page with "Start Test" button
│   │   ├── layout.tsx           # Root layout
│   │   ├── test/
│   │   │   └── page.tsx         # Test interface with navigation
│   │   ├── results/
│   │   │   └── page.tsx         # Results page with explanations
│   │   └── api/
│   │       ├── questions/       # API route for fetching questions
│   │       └── submit/          # API route for grading
│   ├── lib/
│   │   └── database.ts          # Database utility for Next.js
│   ├── package.json             # Node.js dependencies
│   ├── tsconfig.json            # TypeScript configuration
│   └── next.config.js           # Next.js configuration
└── data/                        # Data directory (auto-created)
    ├── questions.db             # SQLite database with all questions
    ├── raw/                     # Downloaded source files
    │   └── discover-canada.pdf
    └── processed/               # Extracted and processed data
        ├── chapters.json        # Extracted PDF chapters
        ├── transcript.json      # YouTube content
        └── test_*.txt           # Generated test files (CLI mode)ment variables
├── .env                         # Your API keys (create from .env.example)
├── README.md                    # This file
├── PLAN.md                      # Development plan
└── data/                        # Data directory (auto-created)
    ├── raw/                     # Downloaded source files
    │   └── discover-canada.pdf
    ├── processed/               # Extracted and processed data
    │   ├── questions.json       # Main question database
    │   ├── llm_generated_questions.json  # LLM-generated questions
    │   ├── chapters.json        # Extracted PDF chapters
    │   ├── transcript.json      # YouTube content
    │   ├── discover-canada-content.txt
    │   ├── test_YYYYMMDD_HHMMSS.txt
    │   └── answers_YYYYMMDD_HHMMSS.txt
    └── cache/                   # Temporary files
```

## 🔧 Configuration

Edit [config.py](config.py) to customize:
- Number of questions per test (default: 20)
- Source URLs
- File paths
- Question types
- LLM provider (OpenAI or Anthropic)
- Questions per chapter for LLM generation

Edit `.env` file to set:
- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `LLM_PROVIDER`: Preferred provider ("openai" or "anthropic")
- `QUESTIONS_PER_CHAPTER`: Number of questions to generate per chapter (default: 10)
- `OPENAI_MODEL`: OpenAI model to use (default: "gpt-4o-mini")
- `ANTHROPIC_MODEL`: Anthropic model to use (default: "claude-3-5-sonnet-20241022")

## � Managing Dependencies

### Workflow 1: Web Application (Recommended)

```powershell
# Step 1: Setup data sources and populate database
uv run python main.py --setup

# Step 2: Generate questions using AI (for PDF content)
uv run python main.py --generate-llm --provider openai

# Step 3: View database statistics
uv run python main.py --stats

# Step 4: Start the web server
cd webapp
npm install
npm run dev
```

Navigate to http://localhost:3000 and:
1. Click "Start Test" to begin
2. Answer 20 randomly selected questions
3. Navigate between questions using Previous/Next buttons
4. Change your answers anytime before submitting
5. Submit to see your score and detailed explanations
6. You pass with 80% or higher (16+ correct out of 20)

### Workflow 2: Command-Line Mode

```powershell
# Generate a 20-question test in CLI
```powershell
uv remove package-name
```

### Update dependencies

```powershell
uv sync --upgrade
```

### View installed packages

```powershell
uv pip list
```

## �📝 Usage Examples

### Workflow 1: Generate Questions with AI (Recommended)

```powershell
# Step 1: Setup data sources
uv run python main.py --setup

# Step 2: Generate questions using AI
uv run python main.py --generate-llm --provider openai

# Step 3: Generate a practice test
uv run python main.py --generate 20
```

### Workflow 2: Interactive Mode

```powershell
uv run python main.py
```

Menu options:
1. Setup/Update data sources
2. Generate questions with LLM (recommended)
3. Generate a new test
4. View question database stats
5. Exit

### Workflow 3: Quick Test Generation

```powershell
# Generate 15-question test (uses existing question database)
uv run python main.py --generate 15

# Generate default 20-question test
uv run python main.py --generate 20
```

### Update Data Sources

```powershell
uv run python main.py --setup
```

This will:
- Download the latest PDF from official website
- Extract YouTube content (subtitles/captions)
- Extract chapters from PDF
- Save to local database

## 🛠️ Troubleshooting

### YouTube Content Extraction

**Issue:** "No captions found" warning

**Solutions:**
1. The video might not have subtitles or auto-captions enabled
2. The video description may still provide useful context
3. Try a different video with captions enabled
4. Update the `YOUTUBE_VIDEO_URL` in [config.py](config.py) to a video with captions

### LLM Question Generation

**Issue:** "API key not found" error

**Solution:**
```powershell
# 1. Copy the example file
cp .env.example .env

# 2. Edit .env and add your API key:
#    OPENAI_API_KEY=sk-your-key-here
#    or
#    ANTHROPIC_API_KEY=sk-ant-your-key-here

# 3. Verify the key is loaded
uv run python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Key loaded!' if os.getenv('OPENAI_API_KEY') else 'Key not found')"
```

**Issue:** "Rate limit exceeded" error

**Solution:**
- Wait a few minutes and try again
- Reduce `QUESTIONS_PER_CHAPTER` in [config.py](config.py) or `.env`
- For OpenAI: Check your usage limits at https://platform.openai.com/usage
- For Anthropic: Check your usage at https://console.anthropic.com/

### PDF Extraction

**Issue:** PDF download fails

**Solution:**
- Check your internet connection
- Verify the PDF URL is still valid in [config.py](config.py)
- Try downloading manually and place in `data/raw/` folder

## 📊 Question Format

Questions are stored in JSON format:

**Basic format:**
```json
{
  "question": "What is the capital of Canada?",
  "type": "multiple_choice",
  "options": ["Toronto", "Ottawa", "Montreal", "Vancouver"],
  "correct_answer": "Ottawa",
  "category": "Geography"
}
```

**LLM-generated format (with additional fields):**
```json
{
  "question": "In what year was the Canadian Constitution patriated?",
  "type": "multiple_choice",
  "options": ["1967", "1982", "1990", "2000"],
  "correct_answer": "1982",
  "category": "History",
  "difficulty": "medium",
  "explanation": "The Constitution was patriated in 1982, giving Canada full sovereignty.",
  "chapter": "Modern Canada",
  "source": "llm_generated"
}
```

## 🎓 Test Output

Generated tests are saved with timestamps:
- `test_20260412_143022.txt` - The test questions
- `answers_20260412_143022.txt` - The answer key with explanations

## 🔄 Workflow

1. **Install & Setup**: Install uv and dependencies, create .env with API keys
2. **Extract Data**: Run `--setup` to download PDF and extract chapters
3. **Generate Questions**: Run `--generate-llm` to create AI-powered questions from content
4. **Generate Test**: Create randomized practice tests with `--generate N`
5. **Practice**: Take the test
6. **Check Answers**: Review the answer key with explanations
7. **Repeat**: Generate new tests as needed

## 📚 Dependencies

Core dependencies:
- `yt-dlp` - Advanced YouTube content extraction (subtitles, captions)
- `pymupdf` (fitz) - Better PDF parsing and chapter detection
- `openai` - OpenAI GPT API for question generation
- `anthropic` - Anthropic Claude API for question generation
- `requests` - Download files from URLs
- `python-dotenv` - Environment variable management

Legacy (optional):
- `youtube-transcript-api` - Basic YouTube transcript extraction
- `PyPDF2` - Basic PDF parsing (replaced by pymupdf)

## 🤝 Contributing

To add new questions:

1. **Using LLM (Recommended)**: Run `uv run python main.py --generate-llm`
2. **Manual editing**: Edit `data/processed/questions.json` directly
3. **Programmatic**: Use the API in [llm_question_generator.py](llm_question_generator.py)

To improve extraction:
- Update URL patterns in [config.py](config.py)
- Modify extraction logic in [data_extractor.py](data_extractor.py)
- Customize LLM prompts in [llm_question_generator.py](llm_question_generator.py)

## 📄 License

This project is for educational purposes to help people prepare for the Canadian citizenship test.

## 🔗 Official Resources

- [Official Citizenship Study Guide - Discover Canada](https://www.canada.ca/en/immigration-refugees-citizenship/corporate/publications-manuals/discover-canada.html)
- [Citizenship Test Information](https://www.canada.ca/en/immigration-refugees-citizenship/services/canadian-citizenship/become-canadian-citizen/citizenship-test.html)
- [Practice Citizenship Test](https://www.canada.ca/en/immigration-refugees-citizenship/services/canadian-citizenship/become-canadian-citizen/citizenship-test/study-guide.html)

## ⚠️ Disclaimer

This is an unofficial study tool. For official information about the Canadian citizenship test, please visit the [Government of Canada website](https://www.canada.ca/en/immigration-refugees-citizenship.html).
- Check internet connection
- Verify video ID is correct

**PDF download failing?**
- Check internet connection
- Verify URL is still valid
- Try manual download and place in `data/raw/`

**No questions available?**
- Run `python main.py --setup` first
- Or use the pre-loaded sample questions
