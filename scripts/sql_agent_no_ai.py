import sqlite3

class SimpleSQLAgent:
    def __init__(self):
        self.db_path = "database/sql_agent_class.db"
        
    def execute_query(self, sql):
        """Execute SQL query"""
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
    
    def manual_query(self):
        """Manual SQL query interface"""
        print("Simple SQL Agent (Manual Mode)")
        print("Type 'exit' to quit")
        
        while True:
            sql = input("\nEnter SQL query: ")
            if sql.lower() == 'exit':
                break
                
            success, result, columns = self.execute_query(sql)
            
            if success:
                if not result:
                    print("No results found.")
                else:
                    print("Results:")
                    for row in result:
                        print(row)
            else:
                print(f"Error: {result}")

if __name__ == "__main__":
    agent = SimpleSQLAgent()
    agent.manual_query()
