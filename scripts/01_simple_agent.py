import google.generativeai as genai
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

class SimpleSQLAgent:
    def __init__(self):
        self.db_path = "database/sql_agent_class.db"
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
    def execute_query(self, sql):
        """Execute any SQL query without restrictions - DANGEROUS!"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(sql)
            if sql.strip().lower().startswith("select"):
                results = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                return True, results, columns
            else:
                conn.commit()
                return True, f"Executed: {sql}. Rows affected: {cursor.rowcount}", None
        except Exception as e:
            return False, str(e), None
        finally:
            conn.close()
    
    def generate_sql(self, question):
        """Use Gemini to convert question to SQL"""
        prompt = f"Convert this to SQL: {question}. Return only SQL code."
        response = self.model.generate_content(prompt)
        return response.text.strip()
    
    def run(self):
        """Run the simple agent"""
        print("Simple SQL Agent - No Security Restrictions")
        print("⚠️  WARNING: This agent can execute ANY SQL including DELETE, DROP, etc.")
        print("Type 'exit' to quit")
        
        while True:
            question = input("\nEnter your question: ")
            if question.lower() == 'exit':
                break
                
            # Get SQL from Gemini
            sql = self.generate_sql(question)
            print(f"Generated SQL: {sql}")
            
            # Execute the query
            success, result, columns = self.execute_query(sql)
            
            if success:
                if columns:  # SELECT query
                    print("Results:")
                    for row in result:
                        print(row)
                else:  # Other query
                    print(f"Success: {result}")
            else:
                print(f"Error: {result}")

if __name__ == "__main__":
    agent = SimpleSQLAgent()
    agent.run()
