"""Main application for Canada Citizenship Test Generator."""

import sys
import argparse
from pathlib import Path
from datetime import datetime

from data_extractor import DataExtractor
from test_generator import TestGenerator
from database import QuestionDatabase
import config


class CitizenshipTestApp:
    """Main application class for the citizenship test generator."""
    
    def __init__(self):
        """Initialize the application."""
        self.extractor = DataExtractor()
        self.generator = TestGenerator()
        self.db = QuestionDatabase()
    
    def setup_data(self):
        """Download and extract all required data sources."""
        print("\n" + "=" * 60)
        print("SETTING UP DATA SOURCES")
        print("=" * 60)
        
        total_questions_added = 0
        
        # Extract YouTube content (pattern matching - no LLM)
        print("\n1. Extracting YouTube questions (pattern matching)...")
        try:
            result = self.extractor.extract_youtube_content()
            if result.get('subtitles') or result.get('auto_captions'):
                text_content = self.extractor.get_youtube_text_content(result)
                print(f"   ✓ Successfully extracted {len(text_content)} characters of content")
                
                # Parse questions from YouTube transcript using pattern matching
                print("   Parsing questions from YouTube transcript...")
                youtube_questions = self.extractor.parse_transcript_for_questions(result)
                if youtube_questions:
                    # Save to database
                    count = self.db.add_questions_bulk(youtube_questions)
                    total_questions_added += count
                    print(f"   ✓ Added {count} questions to database (source: youtube_transcript)")
            else:
                print("   ⚠ Warning: No captions found")
                print(f"   ℹ Title: {result.get('title', 'Unknown')}")
                if result.get('description'):
                    print(f"   ℹ Description available ({len(result['description'])} chars)")
        except Exception as e:
            print(f"   ✗ Error extracting YouTube content: {e}")
        
        # Download and extract PDF
        print("\n2. Downloading and extracting PDF content...")
        try:
            content = self.extractor.extract_pdf_content()
            if content:
                print(f"   ✓ Successfully extracted PDF content")
            else:
                print("   ⚠ Warning: No PDF content extracted")
        except Exception as e:
            print(f"   ✗ Error extracting PDF: {e}")
        
        # Extract chapters from PDF
        print("\n3. Extracting chapters from PDF...")
        try:
            chapters = self.extractor.extract_pdf_chapters()
            if chapters:
                print(f"   ✓ Successfully extracted {len(chapters)} chapters")
            else:
                print("   ⚠ Warning: No chapters found")
        except Exception as e:
            print(f"   ✗ Error extracting chapters: {e}")
        
        print("\n" + "=" * 60)
        print("DATA SETUP COMPLETE")
        print(f"Total questions added to database: {total_questions_added}")
        print(f"Database location: {self.db.db_path}")
        print("=" * 60)
    
    def generate_questions_with_llm(self, provider: str = None):
        """
        Generate questions from PDF using LLM and save to database.
        
        Args:
            provider: LLM provider ("openai" or "anthropic")
        """
        if provider is None:
            provider = config.LLM_PROVIDER
        
        print(f"\n{'=' * 60}")
        print(f"GENERATING QUESTIONS FROM PDF WITH {provider.upper()} LLM")
        print("=" * 60)
        
        try:
            questions = self.extractor.generate_questions_from_pdf(
                provider=provider,
                questions_per_chapter=config.QUESTIONS_PER_CHAPTER
            )
            
            if questions:
                # Save to database
                count = self.db.add_questions_bulk(questions)
                print(f"\n✓ Successfully generated and saved {count} questions to database!")
                print(f"✓ Database location: {self.db.db_path}")
            else:
                print("\n⚠ No questions were generated")
                
        except ValueError as e:
            print(f"\n✗ Error: {e}")
            print("\n💡 To use LLM question generation:")
            print("   1. Copy .env.example to .env")
            print("   2. Add your API key for OpenAI or Anthropic")
            print("   3. Run this command again")
        except Exception as e:
            print(f"\n✗ Error generating questions: {e}")
    
    def generate_test(self, num_questions: int = None, save: bool = True):
        """
        Generate a new test.
        
        Args:
            num_questions: Number of questions (default from config)
            save: Whether to save the test to a file
        """
        if num_questions is None:
            num_questions = config.NUM_QUESTIONS
        
        print(f"\n{'=' * 60}")
        print(f"GENERATING TEST WITH {num_questions} QUESTIONS")
        print("=" * 60)
        
        # Generate test
        test_questions = self.generator.generate_test(num_questions)
        
        # Format for display
        test_output = self.generator.format_test_for_display(test_questions)
        answer_key = self.generator.create_answer_key(test_questions)
        
        # Display
        print("\n" + test_output)
        
        # Save if requested
        if save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_file = config.PROCESSED_DATA_DIR / f"test_{timestamp}.txt"
            answer_file = config.PROCESSED_DATA_DIR / f"answers_{timestamp}.txt"
            
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_output)
            
            with open(answer_file, 'w', encoding='utf-8') as f:
                f.write(answer_key)
            
            print(f"\n✓ Test saved to: {test_file}")
            print(f"✓ Answers saved to: {answer_file}")
        
        # Ask if user wants to see answers
        print("\n" + "=" * 60)
        show_answers = input("Show answer key? (y/n): ").lower()
        if show_answers == 'y':
            print("\n" + answer_key)
    
    def interactive_mode(self):
        """Run the application in interactive mode."""
        print("\n" + "=" * 60)
        print("CANADA CITIZENSHIP TEST GENERATOR")
        print("=" * 60)
        
        while True:
            print("\nOptions:")
            print("1. Setup/Update data sources")
            print("2. Generate questions with LLM (recommended)")
            print("3. Generate a new test")
            print("4. View question database stats")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                self.setup_data()
            elif choice == '2':
                provider = input(f"LLM provider (openai/anthropic, default {config.LLM_PROVIDER}): ").strip().lower()
                if not provider or provider not in ['openai', 'anthropic']:
                    provider = config.LLM_PROVIDER
                self.generate_questions_with_llm(provider)
            elif choice == '3':
                num_q = input(f"Number of questions (default {config.NUM_QUESTIONS}): ").strip()
                num_questions = int(num_q) if num_q.isdigit() else None
                self.generate_test(num_questions)
            elif choice == '4':
                self.show_stats()
            elif choice == '5':
                print("\nGoodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def show_stats(self):
        """Display statistics about the question database."""
        print("\n" + "=" * 60)
        print("QUESTION DATABASE STATISTICS")
        print("=" * 60)
        
        stats = self.db.get_statistics()
        
        print(f"\nTotal questions: {stats['total']}")
        
        print("\nBy source:")
        for source, count in stats['by_source'].items():
            print(f"  {source}: {count}")
        
        print("\nBy category:")
        for category, count in sorted(stats['by_category'].items()):
            print(f"  {category}: {count}")
        
        print(f"\nDatabase location: {self.db.db_path}")
        print("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Canada Citizenship Test Generator"
    )
    parser.add_argument(
        '--setup',
        action='store_true',
        help='Setup/update data sources'
    )
    parser.add_argument(
        '--generate-llm',
        action='store_true',
        help='Generate questions using LLM from PDF chapters'
    )
    parser.add_argument(
        '--provider',
        choices=['openai', 'anthropic'],
        default=None,
        help='LLM provider to use (default: from config)'
    )
    parser.add_argument(
        '--generate',
        type=int,
        metavar='N',
        help='Generate a test with N questions'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show question database statistics'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    args = parser.parse_args()
    app = CitizenshipTestApp()
    
    # If no arguments, run interactive mode
    if len(sys.argv) == 1:
        app.interactive_mode()
        return
    
    # Handle command-line arguments
    if args.setup:
        app.setup_data()
    
    if args.generate_llm:
        provider = args.provider or config.LLM_PROVIDER
        app.generate_questions_with_llm(provider)
    
    if args.generate:
        app.generate_test(args.generate)
    
    if args.stats:
        app.show_stats()
    
    if args.interactive:
        app.interactive_mode()


if __name__ == "__main__":
    main()
