import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

class DangerousSQLAgent:
    def __init__(self):
        self.db_path = "database/sql_agent_class.db"
        
    def execute_any_sql(self, sql):
        """Execute ANY SQL without validation - DANGEROUS!"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(sql)
            if sql.strip().lower().startswith("select"):
                results = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                conn.commit()
                return True, results, columns
            else:
                conn.commit()
                return True, f"Executed: {sql}. Rows affected: {cursor.rowcount}", None
        except Exception as e:
            return False, str(e), None
        finally:
            conn.close()
    
    def demo_dangerous_operations(self):
        """Demonstrate dangerous operations"""
        print("⚠️  DANGEROUS SQL AGENT DEMO - EDUCATIONAL PURPOSES ONLY")
        print("This demonstrates what NOT to do in production!")
        print("Type 'exit' to quit")
        
        # Make a backup first
        self.execute_any_sql("CREATE TABLE customers_backup AS SELECT * FROM customers")
        
        while True:
            sql = input("\nEnter SQL to execute (DANGEROUS!): ")
            if sql.lower() == 'exit':
                break
                
            success, result, columns = self.execute_any_sql(sql)
            
            if success:
                if columns:  # SELECT query
                    print("Results:")
                    for row in result:
                        print(row)
                else:  # Other query
                    print(f"Success: {result}")
            else:
                print(f"Error: {result}")
        
        # Restore from backup
        self.execute_any_sql("DELETE FROM customers")
        self.execute_any_sql("INSERT INTO customers SELECT * FROM customers_backup")
        self.execute_any_sql("DROP TABLE customers_backup")
        print("Database restored to original state")

if __name__ == "__main__":
    agent = DangerousSQLAgent()
    agent.demo_dangerous_operations()
