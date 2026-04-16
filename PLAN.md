# Canada Citizenship Test Generator - Implementation Plan

## 📋 Project Goal

Create an automated system to generate practice tests for the Canadian citizenship exam by:
1. Extracting content from YouTube tutorials
2. Parsing official PDF study materials
3. Building a question database
4. Generating randomized 20-question tests

---

## 🎯 Requirements Analysis

### Functional Requirements
- ✅ Extract transcript from YouTube video
- ✅ Download and parse "Discover Canada" PDF
- ✅ Store questions in a structured format
- ✅ Generate random 20-question tests
- ✅ Support multiple question types (multiple choice, true/false)
- ✅ Provide answer keys
- ✅ Save tests with timestamps

### Non-Functional Requirements
- Easy to use (both CLI and interactive modes)
- Extensible (easy to add new questions)
- Reliable data extraction
- Cross-platform compatibility

---

## 🏗️ Architecture

### Component Breakdown

```
┌─────────────────────────────────────────┐
│         Main Application (main.py)       │
│   - Interactive menu                     │
│   - CLI argument parsing                 │
│   - Workflow orchestration               │
└──────────┬──────────────┬───────────────┘
           │              │
           ▼              ▼
┌──────────────────┐  ┌──────────────────┐
│  Data Extractor  │  │  Test Generator  │
│                  │  │                  │
│ - YouTube API    │  │ - Question DB    │
│ - PDF parser     │  │ - Randomization  │
│ - Text extraction│  │ - Formatting     │
└──────────────────┘  └──────────────────┘
           │              │
           ▼              ▼
┌─────────────────────────────────────────┐
│         Configuration (config.py)        │
│   - Paths, URLs, settings                │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│         Data Directory Structure         │
│   data/                                  │
│   ├── raw/          (source files)       │
│   ├── processed/    (parsed data)        │
│   └── cache/        (temporary)          │
└─────────────────────────────────────────┘
```

### Module Descriptions

#### 1. config.py
- Central configuration
- Path management
- URL definitions
- Settings constants

#### 2. data_extractor.py
- **YouTubeExtractor**: Extract video transcripts
- **PDFExtractor**: Download and parse PDF
- **QuestionParser**: Parse questions from text

#### 3. test_generator.py
- **TestGenerator**: Create randomized tests
- **QuestionDatabase**: Manage questions
- **Formatter**: Format output for display/printing

#### 4. main.py
- **CLI Interface**: Command-line arguments
- **Interactive Menu**: User-friendly wizard
- **Workflow Manager**: Orchestrate operations

---

## 📊 Data Model

### Question Schema

```python
{
    "question": str,           # The question text
    "type": str,              # "multiple_choice" or "true_false"
    "options": List[str],     # For multiple choice
    "correct_answer": Any,    # Answer value
    "category": str,          # Subject category
    "difficulty": str         # Optional: easy/medium/hard
}
```

### Test Schema

```python
{
    "test_id": str,           # Unique identifier
    "timestamp": datetime,    # Generation time
    "num_questions": int,     # Number of questions
    "questions": List[Dict],  # Question objects
    "shuffled": bool          # Whether shuffled
}
```

---

## 🔄 Workflow

### Setup Phase (First-time or Update)

```
1. Check for existing data
   ├─ If not exists: Create directories
   └─ If exists: Ask to update

2. Extract YouTube Transcript
   ├─ Parse video ID from URL
   ├─ Call YouTube Transcript API
   ├─ Save raw transcript (JSON)
   └─ Parse for question patterns

3. Download PDF
   ├─ Fetch from official URL
   ├─ Save to raw directory
   └─ Extract text content

4. Parse Questions
   ├─ Extract from transcript
   ├─ Extract from PDF sections
   └─ Build question database (JSON)

5. Validate
   ├─ Check question format
   ├─ Verify answers present
   └─ Report statistics
```

### Test Generation Phase

```
1. Load Question Database
   ├─ Read questions.json
   └─ Validate format

2. Select Questions
   ├─ Random sample (n=20)
   ├─ Optional: filter by category
   └─ Optional: filter by difficulty

3. Shuffle Options
   ├─ For multiple choice: shuffle answers
   └─ Track correct answer position

4. Format Output
   ├─ Create test file
   ├─ Create answer key
   └─ Save with timestamp

5. Display
   ├─ Show test to user
   └─ Optionally show answers
```

---

## 🛠️ Implementation Steps

### Phase 1: Core Infrastructure ✅
- [x] Create project structure
- [x] Setup configuration system
- [x] Implement data directories
- [x] Create requirements file

### Phase 2: Data Extraction ✅
- [x] YouTube transcript extractor
- [x] PDF downloader
- [x] PDF text parser
- [x] Question pattern recognition

### Phase 3: Test Generation ✅
- [x] Question database structure
- [x] Random selection algorithm
- [x] Answer shuffling
- [x] Test formatting
- [x] Answer key generation

### Phase 4: User Interface ✅
- [x] CLI argument parsing
- [x] Interactive menu system
- [x] Progress indicators
- [x] Error handling

### Phase 5: Sample Data ✅
- [x] Create 25+ sample questions
- [x] Cover all main categories
- [x] Mix question types
- [x] Validate answers

---

## 📦 Dependencies

### Core Libraries
- `youtube-transcript-api==0.6.2` - YouTube transcript extraction
- `PyPDF2==3.0.1` - PDF parsing
- `requests==2.31.0` - HTTP requests
- `python-dotenv==1.0.0` - Environment variables

### Standard Library
- `json` - Data serialization
- `random` - Randomization
- `pathlib` - Path handling
- `argparse` - CLI parsing
- `datetime` - Timestamps

---

## 🧪 Testing Strategy

### Manual Testing
1. Run setup with clean slate
2. Generate multiple tests
3. Verify randomization
4. Check answer keys
5. Test error cases

### Test Scenarios
- ✅ First run (no data)
- ✅ Generate test with default settings
- ✅ Generate test with custom count
- ✅ Update existing data
- ✅ Handle missing dependencies

---

## 🚀 Usage Patterns

### Pattern 1: First-Time User
```powershell
# Install dependencies
pip install -r requirements.txt

# Run interactive mode
python main.py

# Choose: Setup data → Generate test
```

### Pattern 2: Quick Test Generation
```powershell
# One-liner for new test
python main.py --generate 20
```

### Pattern 3: Data Update
```powershell
# Refresh from sources
python main.py --setup
```

---

## 🔮 Future Enhancements

### Potential Features
- [ ] Web interface (Flask/Django)
- [ ] Timed test mode
- [ ] Score tracking and history
- [ ] Difficulty levels
- [ ] Category-specific tests
- [ ] Export to PDF
- [ ] Mobile app
- [ ] Multilingual support (French)
- [ ] Question contribution system
- [ ] AI-generated questions from PDF content

### Advanced Data Extraction
- [ ] Advanced NLP for question extraction
- [ ] Image/diagram questions from PDF
- [ ] Multiple video sources
- [ ] Community question database

---

## 📚 References

- [Official Discover Canada Guide](https://www.canada.ca/content/dam/ircc/migration/ircc/english/pdf/pub/discover-large.pdf)
- [YouTube Tutorial Video](https://www.youtube.com/watch?v=n8JSyQqpSIg)
- [Citizenship Test Information](https://www.canada.ca/en/immigration-refugees-citizenship/services/canadian-citizenship/become-canadian-citizen/citizenship-test.html)

---

## 🎓 Learning Outcomes

This project demonstrates:
- Data extraction from multiple sources
- API integration (YouTube)
- PDF processing
- Random test generation algorithms
- CLI application design
- File I/O and data persistence
- User experience design (interactive menus)
- Error handling and validation

---

## ✅ Current Status

**Phase**: ✅ COMPLETE - All core features implemented

**Last Updated**: April 12, 2026

**Ready for**: Production use, testing, and community feedback
