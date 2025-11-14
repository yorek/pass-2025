import os
from dotenv import load_dotenv
import mssql_python as mssql

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the connection string from environment variable
    connection_string = os.getenv('MSSQL')
    
    if not connection_string:
        print("Error: MSSQL environment variable not found")
        return
    
    try:
        # Connect to the database
        print("Connecting to database...")
        conn = mssql.connect(connection_string)
        cursor = conn.cursor()
        
        # Query to get all tables
        query = """
        SELECT 
            TABLE_SCHEMA,
            TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_SCHEMA, TABLE_NAME
        """
        
        cursor.execute(query)
        tables = cursor.fetchall()
        
        # Display the results
        print(f"\nFound {len(tables)} tables:\n")
        print(f"{'Schema':<20} {'Table Name':<40}")
        print("-" * 60)
        
        for table in tables:
            schema, table_name = table
            print(f"{schema:<20} {table_name:<40}")
        
        # Close the connection
        cursor.close()
        conn.close()
        print("\nConnection closed successfully.")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
