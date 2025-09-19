import sqlite3
import os

def reset_database():
    # Read seed SQL
    with open('database/sql_agent_seed.sql', 'r') as f:
        sql_script = f.read()
    
    # Remove existing database
    db_path = 'database/sql_agent_class.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create new database and execute script
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute each statement separately
    statements = sql_script.split(';')
    for statement in statements:
        if statement.strip():
            try:
                cursor.execute(statement)
            except Exception as e:
                print(f"Error executing: {statement}\nError: {e}")
    
    conn.commit()
    conn.close()
    print("Database reset successfully!")

if __name__ == "__main__":
    reset_database()
