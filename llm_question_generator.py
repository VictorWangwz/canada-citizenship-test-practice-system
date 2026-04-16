"""LLM-powered question generator for Canada Citizenship Test."""

import json
import os
from typing import List, Dict, Optional
from pathlib import Path
import anthropic
from openai import OpenAI
import config


class LLMQuestionGenerator:
    """Uses LLM to generate high-quality questions from text content."""
    
    def __init__(self, provider: str = "openai"):
        """
        Initialize the LLM question generator.
        
        Args:
            provider: LLM provider ("openai" or "anthropic")
        """
        self.provider = provider.lower()
        
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            self.client = OpenAI(api_key=api_key)
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        elif self.provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def generate_questions_from_text(
        self, 
        text: str, 
        num_questions: int = 5,
        difficulty: str = "mixed",
        context: str = ""
    ) -> List[Dict]:
        """
        Generate questions from a text passage.
        
        Args:
            text: Text content to generate questions from
            num_questions: Number of questions to generate
            difficulty: Difficulty level ("easy", "medium", "hard", "mixed")
            context: Additional context about the topic
            
        Returns:
            List of generated questions
        """
        prompt = self._create_question_generation_prompt(
            text, num_questions, difficulty, context
        )
        
        if self.provider == "openai":
            return self._generate_with_openai(prompt)
        else:
            return self._generate_with_anthropic(prompt)
    
    def _create_question_generation_prompt(
        self, 
        text: str, 
        num_questions: int,
        difficulty: str,
        context: str
    ) -> str:
        """Create the prompt for question generation."""
        return f"""You are an expert at creating Canadian citizenship test questions.

Based on the following text content, generate {num_questions} high-quality test questions.

Context: {context if context else "General Canadian citizenship knowledge"}
Difficulty Level: {difficulty}

Text Content:
{text}

Generate questions following these requirements:
1. Mix of question types: multiple choice (4 options), true/false
2. Questions should test different aspects: factual recall, comprehension, application
3. Multiple choice questions should have plausible distractors
4. Vary the question phrasing (What, Who, When, Where, Why, How, Which)
5. Ensure all questions are directly answerable from the text
6. For {difficulty} difficulty:
   - easy: Direct factual questions
   - medium: Require understanding and some inference
   - hard: Require synthesis and deeper comprehension
   - mixed: Combination of all levels

Return ONLY a valid JSON array with this exact structure:
[
  {{
    "question": "Question text here?",
    "type": "multiple_choice",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "category": "Category name",
    "difficulty": "easy|medium|hard",
    "explanation": "Why this is the correct answer"
  }},
  {{
    "question": "Statement here.",
    "type": "true_false",
    "correct_answer": true,
    "category": "Category name",
    "difficulty": "easy|medium|hard",
    "explanation": "Why this is true/false"
  }}
]

Return ONLY the JSON array, no markdown formatting, no additional text."""
    
    def _generate_with_openai(self, prompt: str) -> List[Dict]:
        """Generate questions using OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Canadian citizenship test question generator. Always return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                response_format={ "type": "json_object" }
            )
            
            content = response.choices[0].message.content
            
            # Try to parse as JSON
            try:
                # If wrapped in an object, extract the array
                parsed = json.loads(content)
                if isinstance(parsed, dict):
                    # Look for an array key
                    for key in ['questions', 'items', 'data', 'results']:
                        if key in parsed and isinstance(parsed[key], list):
                            return parsed[key]
                    # If not found, return the values if it's a single question
                    if all(k in parsed for k in ['question', 'type', 'correct_answer']):
                        return [parsed]
                return parsed if isinstance(parsed, list) else []
            except json.JSONDecodeError:
                print(f"Failed to parse OpenAI response as JSON: {content}")
                return []
                
        except Exception as e:
            print(f"Error generating questions with OpenAI: {e}")
            return []
    
    def _generate_with_anthropic(self, prompt: str) -> List[Dict]:
        """Generate questions using Anthropic API."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            content = response.content[0].text
            
            # Clean up markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            # Try to parse as JSON
            try:
                parsed = json.loads(content)
                if isinstance(parsed, dict):
                    # Look for an array key
                    for key in ['questions', 'items', 'data', 'results']:
                        if key in parsed and isinstance(parsed[key], list):
                            return parsed[key]
                    # If not found, return the values if it's a single question
                    if all(k in parsed for k in ['question', 'type', 'correct_answer']):
                        return [parsed]
                return parsed if isinstance(parsed, list) else []
            except json.JSONDecodeError:
                print(f"Failed to parse Anthropic response as JSON: {content}")
                return []
                
        except Exception as e:
            print(f"Error generating questions with Anthropic: {e}")
            return []
    
    def generate_questions_from_chapters(
        self, 
        chapters: List[Dict[str, str]],
        questions_per_chapter: int = 10
    ) -> List[Dict]:
        """
        Generate questions from multiple chapters.
        
        Args:
            chapters: List of dicts with 'title' and 'content' keys
            questions_per_chapter: Number of questions per chapter
            
        Returns:
            List of all generated questions
        """
        all_questions = []
        
        for i, chapter in enumerate(chapters, 1):
            print(f"Generating questions for chapter {i}/{len(chapters)}: {chapter['title']}")
            
            questions = self.generate_questions_from_text(
                text=chapter['content'],
                num_questions=questions_per_chapter,
                difficulty="mixed",
                context=f"Chapter: {chapter['title']}"
            )
            
            # Add chapter info to each question
            for q in questions:
                q['chapter'] = chapter['title']
                q['source'] = 'llm_generated'
            
            all_questions.extend(questions)
            print(f"  Generated {len(questions)} questions")
        
        return all_questions
    
    def save_questions(self, questions: List[Dict], filepath: Path):
        """Save generated questions to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(questions)} questions to {filepath}")


if __name__ == "__main__":
    # Test the generator
    from dotenv import load_dotenv
    load_dotenv()
    
    # Test with sample text
    sample_text = """
    Canada became a nation on July 1, 1867, when the British North America Act was passed.
    The capital of Canada is Ottawa, located in the province of Ontario. Canada has two official
    languages: English and French. The country consists of 10 provinces and 3 territories.
    The current head of state is the Monarch, represented by the Governor General.
    """
    
    generator = LLMQuestionGenerator(provider="openai")
    questions = generator.generate_questions_from_text(sample_text, num_questions=5)
    
    print("\n=== Generated Questions ===")
    print(json.dumps(questions, indent=2))
