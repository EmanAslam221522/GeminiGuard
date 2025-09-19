import sqlite3

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

print("Basic SQL Tool")
print("Type 'exit' to quit")

while True:
    sql = input("\nEnter SQL query: ")
    if sql.lower() == 'exit':
        break
        
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
