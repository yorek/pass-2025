import os, json
import mssql_python as mssql
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    connection = mssql.connect(os.getenv("MSSQL"))
    cursor = connection.cursor()
    with cursor.execute("SELECT JSON_OBJECT('ServerName': @@servername, 'DatabaseName': DB_NAME(), 'UserName': USER_NAME()) AS Info"):
        result = json.loads(cursor.fetchone()[0])
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

