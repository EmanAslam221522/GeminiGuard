import google.generativeai as genai
import sqlite3
import re

# Hardcode your API key directly
API_KEY = "AIzaSyB8YKVmzAN7M5yZ2B9VX6EtPPalsBOLRH0"

# Configure Gemini
genai.configure(api_key=API_KEY)

# Use an available model
model = genai.GenerativeModel('gemini-1.5-flash-latest')

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
    # First, get the database schema
    conn = sqlite3.connect('database/sql_agent_class.db')
    cursor = conn.cursor()
    
    # Get table info
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    
    schema_info = "Database tables: " + ", ".join(tables)
    conn.close()
    
    prompt = f"""
    Database schema: {schema_info}
    
    Convert this natural language query to SQL:
    "{question}"
    
    Return only the SQL query without any explanation or formatting.
    Use proper SQLite syntax.
    """
    
    try:
        response = model.generate_content(prompt)
        sql_query = response.text.strip()
        # Clean up the response
        sql_query = re.sub(r"```sql|```", "", sql_query).strip()
        return sql_query, None
    except Exception as e:
        return None, str(e)

print("SQL Agent with Gemini (Working Version)")
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
