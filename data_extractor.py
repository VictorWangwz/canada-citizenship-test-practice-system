"""Module for extracting data from YouTube and PDF sources."""

import json
import requests
from pathlib import Path
import yt_dlp
import fitz  # PyMuPDF
import re
from typing import List, Dict, Optional
import config
from llm_question_generator import LLMQuestionGenerator


class DataExtractor:
    """Handles extraction of data from various sources."""
    
    def __init__(self):
        """Initialize the data extractor."""
        self.pdf_path = config.PDF_PATH
        self.youtube_url = config.YOUTUBE_VIDEO_URL
        self.transcript_json = config.TRANSCRIPT_JSON
        self.llm_generator = None
        
    def extract_youtube_content(self, url: str = None) -> Dict:
        """
        Extract content from YouTube video using multiple methods.
        Tries subtitles first, then auto-captions, then description.
        
        Args:
            url: YouTube video URL (uses config if not provided)
            
        Returns:
            Dict with extracted content and metadata
        """
        if url is None:
            url = self.youtube_url
        
        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'skip_download': True,
            'quiet': True,
            'no_warnings': True,
        }
        
        result = {
            'url': url,
            'subtitles': None,
            'auto_captions': None,
            'description': None,
            'title': None,
            'duration': None,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Extracting content from YouTube: {url}")
                info = ydl.extract_info(url, download=False)
                
                result['title'] = info.get('title', '')
                result['description'] = info.get('description', '')
                result['duration'] = info.get('duration', 0)
                
                # Try to get manual subtitles first
                if 'subtitles' in info and 'en' in info['subtitles']:
                    subtitle_url = info['subtitles']['en'][0]['url']
                    subtitle_content = requests.get(subtitle_url).text
                    result['subtitles'] = self._parse_subtitles(subtitle_content)
                    print(f"  ✓ Found manual English subtitles")
                
                # Try automatic captions if no manual subtitles
                elif 'automatic_captions' in info and 'en' in info['automatic_captions']:
                    for format in info['automatic_captions']['en']:
                        if format['ext'] == 'json3':
                            caption_url = format['url']
                            caption_content = requests.get(caption_url).json()
                            result['auto_captions'] = self._parse_json3_captions(caption_content)
                            print(f"  ✓ Found automatic captions")
                            break
                
                # Save to JSON
                with open(self.transcript_json, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                print(f"  ✓ Content saved to {self.transcript_json}")
                return result
                
        except Exception as e:
            print(f"  ✗ Error extracting YouTube content: {e}")
            print(f"  💡 Tip: The video might not have captions available.")
            print(f"     Consider using the video description or finding an alternative source.")
            return result
    
    def _parse_subtitles(self, subtitle_text: str) -> List[Dict]:
        """Parse VTT/SRT subtitle format."""
        lines = subtitle_text.split('\n')
        subtitles = []
        current_text = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('WEBVTT') or '-->' in line or line.isdigit():
                if current_text:
                    subtitles.append({'text': ' '.join(current_text)})
                    current_text = []
            else:
                current_text.append(line)
        
        return subtitles
    
    def _parse_json3_captions(self, caption_data: Dict) -> List[Dict]:
        """Parse YouTube JSON3 caption format."""
        subtitles = []
        
        if 'events' in caption_data:
            for event in caption_data['events']:
                if 'segs' in event:
                    text = ''.join(seg.get('utf8', '') for seg in event['segs'])
                    if text.strip():
                        subtitles.append({
                            'text': text.strip(),
                            'start': event.get('tStartMs', 0) / 1000,
                            'duration': event.get('dDurationMs', 0) / 1000
                        })
        
        return subtitles
    
    def get_youtube_text_content(self, result: Dict = None) -> str:
        """
        Get combined text content from YouTube extraction result.
        
        Args:
            result: Extraction result dict (loads from file if not provided)
            
        Returns:
            Combined text content
        """
        if result is None:
            if self.transcript_json.exists():
                with open(self.transcript_json, 'r', encoding='utf-8') as f:
                    result = json.load(f)
            else:
                return ""
        
        text_parts = []
        
        # Add title and description
        if result.get('title'):
            text_parts.append(f"Title: {result['title']}\n")
        
        if result.get('description'):
            text_parts.append(f"Description: {result['description']}\n")
        
        # Add subtitles/captions
        if result.get('subtitles'):
            text_parts.append("\nSubtitles:")
            text_parts.append(' '.join(item['text'] for item in result['subtitles']))
        elif result.get('auto_captions'):
            text_parts.append("\nAuto-captions:")
            text_parts.append(' '.join(item['text'] for item in result['auto_captions']))
        
        return '\n'.join(text_parts)
    
    def _extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL."""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'^([0-9A-Za-z_-]{11})$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise ValueError(f"Could not extract video ID from URL: {url}")
    
    def download_pdf(self) -> bool:
        """
        Download the Discover Canada PDF.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Downloading PDF from {config.DISCOVER_CANADA_PDF_URL}")
            response = requests.get(config.DISCOVER_CANADA_PDF_URL, stream=True)
            response.raise_for_status()
            
            with open(self.pdf_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"PDF downloaded to {self.pdf_path}")
            return True
        except Exception as e:
            print(f"Error downloading PDF: {e}")
            return False
    
    def extract_pdf_content(self) -> str:
        """
        Extract text content from the Discover Canada PDF using PyMuPDF.
        
        Returns:
            Extracted text content
        """
        if not self.pdf_path.exists():
            print("PDF not found. Downloading...")
            self.download_pdf()
        
        try:
            print(f"Extracting content from {self.pdf_path}")
            doc = fitz.open(self.pdf_path)
            text_content = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text_content.append(page.get_text())
            
            doc.close()
            full_text = "\n".join(text_content)
            
            # Save to text file
            text_file = config.PROCESSED_DATA_DIR / "discover-canada-content.txt"
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(full_text)
            
            print(f"  ✓ PDF content extracted ({len(full_text)} characters)")
            print(f"  ✓ Saved to {text_file}")
            return full_text
        except Exception as e:
            print(f"  ✗ Error extracting PDF content: {e}")
            return ""
    
    def extract_pdf_chapters(self) -> List[Dict[str, str]]:
        """
        Extract chapters/sections from the PDF with improved parsing.
        
        Returns:
            List of dicts with 'title' and 'content' keys
        """
        if not self.pdf_path.exists():
            print("PDF not found. Downloading...")
            self.download_pdf()
        
        try:
            print(f"Extracting chapters from {self.pdf_path}")
            doc = fitz.open(self.pdf_path)
            
            # Get table of contents
            toc = doc.get_toc()
            chapters = []
            
            if toc:
                # Use TOC to extract chapters
                for i, (level, title, page_num) in enumerate(toc):
                    if level == 1:  # Main chapters only
                        # Find the next chapter to know where this one ends
                        next_page = toc[i + 1][2] if i + 1 < len(toc) else len(doc)
                        
                        # Extract text from this chapter
                        chapter_text = []
                        for p in range(page_num - 1, next_page - 1):
                            if p < len(doc):
                                chapter_text.append(doc[p].get_text())
                        
                        chapters.append({
                            'title': title.strip(),
                            'content': '\n'.join(chapter_text),
                            'start_page': page_num,
                            'end_page': next_page - 1
                        })
                        print(f"  ✓ Extracted chapter: {title}")
            
            else:
                # Fallback: Split by detected headings
                print("  ⚠ No TOC found. Attempting to detect chapters by text patterns...")
                chapters = self._detect_chapters_by_text(doc)
            
            doc.close()
            
            # Save chapters to JSON
            chapters_file = config.PROCESSED_DATA_DIR / "chapters.json"
            with open(chapters_file, 'w', encoding='utf-8') as f:
                json.dump(chapters, f, indent=2, ensure_ascii=False)
            
            print(f"  ✓ Extracted {len(chapters)} chapters")
            print(f"  ✓ Saved to {chapters_file}")
            
            return chapters
            
        except Exception as e:
            print(f"  ✗ Error extracting chapters: {e}")
            return []
    
    def _detect_chapters_by_text(self, doc) -> List[Dict[str, str]]:
        """Detect chapters by analyzing text patterns."""
        chapters = []
        current_chapter = None
        current_content = []
        
        # Pattern for chapter headings (typically large, bold, or all caps)
        chapter_pattern = re.compile(r'^([A-Z][A-Z\s]{5,}|Chapter\s+\d+.*)', re.MULTILINE)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            # Look for chapter headings
            matches = chapter_pattern.finditer(text)
            for match in matches:
                heading = match.group(1).strip()
                
                # Save previous chapter
                if current_chapter and current_content:
                    chapters.append({
                        'title': current_chapter,
                        'content': '\n'.join(current_content)
                    })
                
                # Start new chapter
                current_chapter = heading
                current_content = [text[match.end():]]
                break
            else:
                # No heading found, add to current chapter
                if current_chapter:
                    current_content.append(text)
        
        # Add last chapter
        if current_chapter and current_content:
            chapters.append({
                'title': current_chapter,
                'content': '\n'.join(current_content)
            })
        
        return chapters
    
    def generate_questions_from_pdf(
        self, 
        provider: str = "openai",
        questions_per_chapter: int = 10
    ) -> List[Dict]:
        """
        Generate questions from PDF using LLM.
        
        Args:
            provider: LLM provider ("openai" or "anthropic")
            questions_per_chapter: Number of questions to generate per chapter
            
        Returns:
            List of generated questions
        """
        # Extract chapters
        chapters = self.extract_pdf_chapters()
        
        if not chapters:
            print("  ✗ No chapters found. Cannot generate questions.")
            return []
        
        # Initialize LLM generator
        try:
            if self.llm_generator is None:
                self.llm_generator = LLMQuestionGenerator(provider=provider)
            
            # Generate questions for each chapter
            all_questions = self.llm_generator.generate_questions_from_chapters(
                chapters=chapters,
                questions_per_chapter=questions_per_chapter
            )
            
            # Save generated questions
            questions_file = config.PROCESSED_DATA_DIR / "llm_generated_questions.json"
            self.llm_generator.save_questions(all_questions, questions_file)
            
            return all_questions
            
        except Exception as e:
            print(f"  ✗ Error generating questions: {e}")
            print(f"  💡 Make sure you have set your API key in .env file")
            return []
    
    def parse_transcript_for_questions(self, result: Dict = None, debug: bool = False) -> List[Dict]:
        """
        Parse YouTube transcript to extract structured questions.
        Handles the specific format: "Question X: ... A ... B ... C ... D ... The answer is X"
        
        Args:
            result: YouTube extraction result dict (loads from file if not provided)
            debug: If True, print detailed debug information
            
        Returns:
            List of structured question dictionaries
        """
        if result is None:
            # Load from saved file
            if self.transcript_json.exists():
                with open(self.transcript_json, 'r', encoding='utf-8') as f:
                    result = json.load(f)
            else:
                print("No transcript found. Please extract first.")
                return []
        
        # Get captions/subtitles
        captions = result.get('subtitles') or result.get('auto_captions') or []
        if not captions:
            print("No captions found in transcript.")
            return []
        
        # Combine all text
        full_text = " ".join([item['text'] for item in captions])
        
        if debug:
            print(f"Total transcript length: {len(full_text)} characters")
        
        # Parse questions using the improved format parser
        questions = self._parse_youtube_quiz_format(full_text, debug=debug)
        
        if questions:
            print(f"  ✓ Extracted {len(questions)} questions from YouTube transcript")
            
            # Save parsed questions
            questions_file = config.PROCESSED_DATA_DIR / "youtube_questions.json"
            with open(questions_file, 'w', encoding='utf-8') as f:
                json.dump(questions, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Saved to {questions_file}")
        else:
            print("  ⚠ No questions found in transcript")
        
        return questions
    
    def _parse_youtube_quiz_format(self, text: str, debug: bool = False) -> List[Dict]:
        """
        Parse questions from YouTube quiz format.
        Format: Question X. <text>? A. <opt>, B. <opt>, C. <opt>, D. <opt>. The answer is <X>. <explanation>
        
        Args:
            text: Combined transcript text
            debug: If True, print debug information about skipped questions
            
        Returns:
            List of question dictionaries
        """
        questions = []
        current_chapter = "General"
        skipped_reasons = {}
        
        # Find all question boundaries - more flexible pattern
        question_pattern = r'[Qq]uestion\s+(\d+)[,\.\s:\-]*'
        question_matches = list(re.finditer(question_pattern, text))
        
        if debug:
            print(f"\n=== Parsing Debug Info ===")
            print(f"Found {len(question_matches)} question markers")
        
        for i, match in enumerate(question_matches):
            question_num = match.group(1)
            skip_reason = None
            
            try:
                # Get the segment for this question
                start_pos = match.end()
                end_pos = question_matches[i + 1].start() if i + 1 < len(question_matches) else len(text)
                segment = text[start_pos:end_pos].strip()
                
                # Extract chapter if mentioned before this question
                chapter_search_start = max(0, match.start() - 300)
                chapter_match = re.search(r'Chapter\s+(\d+)[,\s:\-]+([^Q]+?)(?=[Qq]uestion)', 
                                         text[chapter_search_start:match.start()], re.IGNORECASE)
                if chapter_match:
                    current_chapter = f"Chapter {chapter_match.group(1)}: {chapter_match.group(2).strip()}"
                
                # Find where options start - more flexible patterns
                options_start = re.search(r'[?\.\s]\s*A[.\s,:\-]+', segment)
                if not options_start:
                    # Try alternate pattern without question mark
                    options_start = re.search(r'\s+A[.\s,:\-]+', segment)
                
                if not options_start:
                    skip_reason = "no_options_start"
                    continue
                
                # Question text is everything before options
                question_text = segment[:options_start.start()].strip()
                
                # Options section is from A to "The answer" - more flexible
                answer_start = re.search(r'[Tt]he\s+answer\s+is', segment)
                if not answer_start:
                    # Try alternate patterns
                    answer_start = re.search(r'[Aa]nswer[:\s]+is', segment)
                
                if not answer_start:
                    skip_reason = "no_answer_marker"
                    continue
                
                options_section = segment[options_start.start():answer_start.start()].strip()
                
                # Extract options with multiple strategies
                options = self._extract_options_flexible(options_section, debug=(debug and i < 5))
                if len(options) != 4:
                    skip_reason = f"wrong_option_count_{len(options)}"
                    continue
                
                # Extract answer letter - more flexible
                answer_section = segment[answer_start.start():]
                answer_match = re.search(r'answer\s+is\s+([A-Da-d])[.\s,]', answer_section, re.IGNORECASE)
                if not answer_match:
                    # Try without punctuation
                    answer_match = re.search(r'answer\s+is\s+([A-Da-d])', answer_section, re.IGNORECASE)
                
                if not answer_match:
                    skip_reason = "no_answer_letter"
                    continue
                
                answer_letter = answer_match.group(1).upper()
                answer_index = ord(answer_letter) - ord('A')
                
                if answer_index >= len(options) or answer_index < 0:
                    skip_reason = f"invalid_answer_index_{answer_index}"
                    continue
                
                correct_answer = options[answer_index]
                
                # Extract explanation (text after the answer) - more flexible
                explanation = ""
                # Look for explanation after answer letter
                explanation_match = re.search(r'answer\s+is\s+[A-Da-d][.\s,]*(.+)', answer_section, re.IGNORECASE | re.DOTALL)
                if explanation_match:
                    explanation = explanation_match.group(1).strip()
                    # Clean up - remove answer text repetition
                    explanation = re.sub(r'^[A-D][.\s]*', '', explanation, flags=re.IGNORECASE)
                    explanation = re.sub(r'\s+', ' ', explanation).strip()
                
                # Clean up question text
                question_text = re.sub(r'\s+', ' ', question_text).strip()
                # Remove leading punctuation
                question_text = re.sub(r'^[,\.\s]+', '', question_text)
                if question_text and not question_text.endswith('?'):
                    question_text += '?'
                
                # Validate question has reasonable content
                if len(question_text) < 10:
                    skip_reason = "question_too_short"
                    continue
                
                # Build question object
                question_obj = {
                    "question": question_text,
                    "type": "multiple_choice",
                    "options": options,
                    "correct_answer": correct_answer,
                    "category": current_chapter,
                    "source": "youtube_transcript",
                    "question_number": int(question_num)
                }
                
                if explanation and len(explanation) > 5:
                    question_obj["explanation"] = explanation
                
                questions.append(question_obj)
                
            except Exception as e:
                skip_reason = f"exception_{type(e).__name__}"
                if debug and i < 10:
                    print(f"  Q{question_num}: Exception - {e}")
            
            # Track skip reasons
            if skip_reason:
                skipped_reasons[skip_reason] = skipped_reasons.get(skip_reason, 0) + 1
        
        if debug:
            print(f"\n=== Parsing Results ===")
            print(f"Successfully parsed: {len(questions)} questions")
            print(f"Skipped: {len(question_matches) - len(questions)} questions")
            if skipped_reasons:
                print("\nSkip reasons:")
                for reason, count in sorted(skipped_reasons.items(), key=lambda x: -x[1]):
                    print(f"  {reason}: {count}")
        
        return questions
    
    def _extract_options_improved(self, options_text: str) -> List[str]:
        """
        Improved option extraction that handles the specific format of this transcript.
        Format: A. option1. B. option2. C. option3. D. option4.
        
        Args:
            options_text: Text containing all four options
            
        Returns:
            List of exactly 4 option strings, or empty list if not found
        """
        # Clean the text
        options_text = options_text.strip()
        
        # More precise pattern: Look for standalone letter markers
        # Use word boundary or specific delimiters to avoid matching in middle of words
        # Pattern: Letter (A-D) + period + text until we see ". <NextLetter>." or end
        pattern = r'\b([A-D])\.\s+(.+?)(?=\s+[A-D]\.|$)'
        matches = list(re.finditer(pattern, options_text, re.IGNORECASE))
        
        option_dict = {}
        for match in matches:
            letter = match.group(1).upper()
            text = match.group(2).strip()
            # Remove trailing period
            text = re.sub(r'\.$', '', text).strip()
            if text and len(text) > 0:
                option_dict[letter] = text
        
        # Build options list in order
        options = []
        for letter in ['A', 'B', 'C', 'D']:
            if letter in option_dict:
                options.append(option_dict[letter])
        
        return options if len(options) == 4 else []
    
    def _extract_options_flexible(self, options_text: str, debug: bool = False) -> List[str]:
        """
        More flexible option extraction with multiple fallback strategies.
        
        Args:
            options_text: Text containing the options
            debug: If True, print debug info
            
        Returns:
            List of option strings (ideally 4)
        """
        options_text = options_text.strip()
        
        # Strategy 1: Standard pattern with period (A. option B. option)
        pattern1 = r'([A-D])\.\s*([^A-D]+?)(?=\s*[A-D]\.|$)'
        matches1 = list(re.finditer(pattern1, options_text, re.IGNORECASE))
        
        option_dict = {}
        for match in matches1:
            letter = match.group(1).upper()
            text = match.group(2).strip()
            # Clean up trailing punctuation
            text = re.sub(r'[,\.\s]+$', '', text).strip()
            if text and len(text) > 0:
                option_dict[letter] = text
        
        if len(option_dict) == 4:
            return [option_dict[l] for l in ['A', 'B', 'C', 'D']]
        
        # Strategy 2: Try with comma or other separators
        if len(option_dict) < 4:
            pattern2 = r'([A-D])[\.\s,]+([^A-D]{3,}?)(?=[,\s]*[A-D][\.\s,]|$)'
            matches2 = list(re.finditer(pattern2, options_text, re.IGNORECASE))
            
            option_dict = {}
            for match in matches2:
                letter = match.group(1).upper()
                text = match.group(2).strip()
                text = re.sub(r'[,\.\s]+$', '', text).strip()
                if text and len(text) > 0:
                    option_dict[letter] = text
            
            if len(option_dict) == 4:
                return [option_dict[l] for l in ['A', 'B', 'C', 'D']]
        
        # Strategy 3: Look for letter followed by text, more aggressively
        if len(option_dict) < 4:
            # Split on letter markers
            parts = re.split(r'\s*([A-D])[\.\s,:]+', options_text, flags=re.IGNORECASE)
            option_dict = {}
            
            for i in range(1, len(parts), 2):
                if i + 1 < len(parts):
                    letter = parts[i].upper()
                    text = parts[i + 1].strip()
                    text = re.sub(r'[,\.\s]+$', '', text).strip()
                    if text and letter in ['A', 'B', 'C', 'D']:
                        option_dict[letter] = text
            
            if len(option_dict) == 4:
                return [option_dict[l] for l in ['A', 'B', 'C', 'D']]
        
        if debug:
            print(f"  Option extraction: found {len(option_dict)}/4 options")
            print(f"  Text: {options_text[:200]}...")
        
        # Return what we have, even if not 4
        return [option_dict.get(l, '') for l in ['A', 'B', 'C', 'D'] if l in option_dict]


if __name__ == "__main__":
    # Test the extractor
    extractor = DataExtractor()
    
    # Extract YouTube transcript
    print("\n=== Extracting YouTube Transcript ===")
    transcript = extractor.extract_youtube_transcript()
    
    # Download and extract PDF
    print("\n=== Extracting PDF Content ===")
    pdf_content = extractor.extract_pdf_content()
    
    # Parse questions
    print("\n=== Parsing Questions ===")
    questions = extractor.parse_transcript_for_questions()
    print(f"Found {len(questions)} potential questions")
