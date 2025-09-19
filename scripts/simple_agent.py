import google.generativeai as genai
import sqlite3

# Hardcode your API key directly
API_KEY = "AIzaSyB8YKVmzAN7M5yZ2B9VX6EtPPalsBOLRH0"

# Configure Gemini
genai.configure(api_key=API_KEY)

# Use a different model name that might work better
try:
    model = genai.GenerativeModel('gemini-pro')
except:
    # Try alternative model names
    try:
        model = genai.GenerativeModel('gemini-1.0-pro')
    except:
        model = genai.GenerativeModel('models/gemini-pro')

def execute_query(sql):
    """Execute SQL query and return results"""
    conn = sqlite3.connect('database/sql_agent_class.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        return results, columns, None
    except Exception as e:
        return None, None, str(e)
    finally:
        conn.close()

def ask_gemini(question):
    """Ask Gemini to convert question to SQL"""
    prompt = f"Convert this to SQL: {question}. Return only SQL code."
    try:
        response = model.generate_content(prompt)
        return response.text.strip(), None
    except Exception as e:
        return None, str(e)

print("Simple SQL Agent with Gemini")
print("Type 'exit' to quit")

while True:
    question = input("\nEnter your question: ")
    if question.lower() == 'exit':
        break
        
    # Get SQL from Gemini
    sql, error = ask_gemini(question)
    
    if error:
        print(f"Error from Gemini: {error}")
        continue
        
    print(f"Generated SQL: {sql}")
    
    # Execute the query
    results, columns, error = execute_query(sql)
    
    if error:
        print(f"SQL Error: {error}")
    elif not results:
        print("No results found")
    else:
        print("Results:")
        for row in results:
            print(row)
