import google.generativeai as genai
import sqlite3
import re
import os
from dotenv import load_dotenv

load_dotenv()

class AnalyticsSQLAgent:
    def __init__(self):
        self.db_path = "database/sql_agent_class.db"
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
    def validate_sql(self, sql):
        """Validate SQL to prevent malicious queries"""
        # Multi-layer validation approach
        if re.search(r"\b(INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|REPLACE)\b", sql, re.I):
            return False, "Write operations are not allowed."
        
        if ";" in sql.replace(";", "", 1):
            return False, "Multiple statements are not allowed."
            
        if not re.match(r"(?is)^\s*select\b", sql):
            return False, "Only SELECT statements are allowed."
            
        return True, "Valid SQL"
    
    def execute_safe_query(self, sql):
        """Execute SQL query with safety checks"""
        # Add LIMIT if not present to prevent large results
        if not re.search(r"\blimit\s+\d+\b", sql, re.I):
            sql += " LIMIT 100"
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return True, results, columns
        except Exception as e:
            return False, str(e), None
        finally:
            conn.close()
    
    def generate_sql_from_natural_language(self, query):
        """Use Gemini to convert natural language to SQL"""
        # Get database schema for context
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema_info = "Database schema:\n"
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            schema_info += f"Table {table_name}:\n"
            for col in columns:
                schema_info += f"  {col[1]} ({col[2]})\n"
        
        conn.close()
        
        # Create prompt for Gemini with analytics focus
        prompt = f"""
        {schema_info}
        
        Based on the database schema above, convert this business analytics question to SQL:
        "{query}"
        
        Focus on business analytics queries like:
        - Revenue calculations
        - Customer segmentation
        - Product performance
        - Time series analysis
        - Multi-table JOINs for comprehensive analysis
        
        Return only the SQL query without any explanation or formatting.
        Make sure to use proper SQLite syntax and only SELECT statements.
        """
        
        try:
            response = self.model.generate_content(prompt)
            sql_query = response.text.strip()
            # Clean up the response
            sql_query = re.sub(r"```sql|```", "", sql_query).strip()
            return sql_query
        except Exception as e:
            return f"Error generating SQL: {str(e)}"
    
    def query(self, natural_language_query):
        """Main method to process natural language queries"""
        # Generate SQL from natural language
        sql = self.generate_sql_from_natural_language(natural_language_query)
        
        if sql.startswith("Error"):
            return sql
            
        # Validate SQL
        is_valid, validation_msg = self.validate_sql(sql)
        if not is_valid:
            return f"Invalid SQL: {validation_msg}\nGenerated SQL: {sql}"
        
        # Execute query
        success, result, columns = self.execute_safe_query(sql)
        
        if success:
            # Format results
            if not result:
                return "No results found."
                
            # Format as table
            header = " | ".join(columns)
            separator = "-" * len(header)
            rows = []
            for row in result:
                rows.append(" | ".join(str(cell) for cell in row))
            
            return f"SQL: {sql}\n\nResults:\n{header}\n{separator}\n" + "\n".join(rows)
        else:
            return f"Error executing query: {result}\nGenerated SQL: {sql}"

# CLI interface
def main():
    agent = AnalyticsSQLAgent()
    
    print("Analytics SQL Agent with Gemini - Business Intelligence")
    print("Type 'exit' to quit")
    print("\nTry questions like:")
    print("- What is our total revenue?")
    print("- Which products are performing best?")
    print("- Show me customer lifetime value")
    print("- What are our monthly sales trends?")
    
    while True:
        query = input("\nEnter your analytics question: ")
        if query.lower() == 'exit':
            break
            
        result = agent.query(query)
        print(f"\n{result}")

if __name__ == "__main__":
    main()
