"""Configuration settings for the Canada Citizenship Test Generator."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CACHE_DIR = DATA_DIR / "cache"

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, CACHE_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# Source URLs
YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v=n8JSyQqpSIg"
DISCOVER_CANADA_PDF_URL = "https://www.canada.ca/content/dam/ircc/migration/ircc/english/pdf/pub/discover-large.pdf"

# File paths
PDF_PATH = RAW_DATA_DIR / "discover-canada.pdf"
QUESTIONS_JSON = PROCESSED_DATA_DIR / "questions.json"
TRANSCRIPT_JSON = PROCESSED_DATA_DIR / "transcript.json"

# Test generation settings
NUM_QUESTIONS = 20
QUESTION_TYPES = ["multiple_choice", "true_false"]

# LLM Settings
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "openai" or "anthropic"
QUESTIONS_PER_CHAPTER = int(os.getenv("QUESTIONS_PER_CHAPTER", "10"))

# API Keys (loaded from environment)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
