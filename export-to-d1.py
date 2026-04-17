# Export SQLite Database to D1-Compatible SQL
# Run this to generate SQL insert statements for D1

import sqlite3
import json

# Connect to SQLite database
conn = sqlite3.connect('data/questions.db')
cursor = conn.cursor()

# Fetch all questions
cursor.execute('SELECT * FROM questions')
rows = cursor.fetchall()

# Get column names
column_names = [description[0] for description in cursor.description]

# Generate SQL file
with open('migrations/data.sql', 'w', encoding='utf-8') as f:
    f.write("-- Data import for Cloudflare D1\n")
    f.write("-- Generated from SQLite database\n\n")
    
    for row in rows:
        # Create a dictionary of column:value pairs
        data = dict(zip(column_names, row))
        
        # Escape single quotes in text fields
        def escape_sql(value):
            if value is None:
                return 'NULL'
            if isinstance(value, str):
                return "'" + value.replace("'", "''") + "'"
            return str(value)
        
        # Build INSERT statement
        question = escape_sql(data['question'])
        type_val = escape_sql(data['type'])
        options = escape_sql(data['options'])
        correct_answer = escape_sql(data['correct_answer'])
        category = escape_sql(data.get('category'))
        difficulty = escape_sql(data.get('difficulty'))
        explanation = escape_sql(data.get('explanation'))
        source = escape_sql(data.get('source'))
        chapter = escape_sql(data.get('chapter'))
        question_number = data.get('question_number') if data.get('question_number') else 'NULL'
        
        sql = f"""INSERT INTO questions (question, type, options, correct_answer, category, difficulty, explanation, source, chapter, question_number) 
VALUES ({question}, {type_val}, {options}, {correct_answer}, {category}, {difficulty}, {explanation}, {source}, {chapter}, {question_number});\n"""
        
        f.write(sql)

conn.close()

print("✓ Generated migrations/data.sql")
print(f"✓ Exported {len(rows)} questions")
print("\nNext steps:")
print("1. Install Wrangler: npm install -g wrangler")
print("2. Login to Cloudflare: wrangler login")
print("3. Create D1 database: wrangler d1 create citizenship-test-db")
print("4. Import schema: wrangler d1 execute citizenship-test-db --file=migrations/schema.sql")
print("5. Import data: wrangler d1 execute citizenship-test-db --file=migrations/data.sql")
