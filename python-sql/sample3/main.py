import os
from flask import Flask, render_template
from dotenv import load_dotenv
import mssql_python as mssql

# Load environment variables
load_dotenv()

app = Flask(__name__)

def get_table_sizes():
    """Get top 25 tables with their sizes from SQL Server"""
    connection_string = os.getenv('MSSQL')
    
    query = """
    SELECT TOP 25
        t.TABLE_SCHEMA + '.' + t.TABLE_NAME AS TableName,
        p.rows AS [RowCount],
        CAST(ROUND(((SUM(a.total_pages) * 8) / 1024.00), 2) AS NUMERIC(36, 2)) AS TotalSpaceMB,
        CAST(ROUND(((SUM(a.used_pages) * 8) / 1024.00), 2) AS NUMERIC(36, 2)) AS UsedSpaceMB,
        CAST(ROUND(((SUM(a.total_pages) - SUM(a.used_pages)) * 8) / 1024.00, 2) AS NUMERIC(36, 2)) AS UnusedSpaceMB
    FROM 
        INFORMATION_SCHEMA.TABLES t
    INNER JOIN      
        sys.tables st ON t.TABLE_NAME = st.name
    INNER JOIN      
        sys.indexes i ON st.OBJECT_ID = i.object_id
    INNER JOIN 
        sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
    INNER JOIN 
        sys.allocation_units a ON p.partition_id = a.container_id
    WHERE 
        t.TABLE_TYPE = 'BASE TABLE'
        AND i.OBJECT_ID > 255
        AND i.index_id <= 1
    GROUP BY 
        t.TABLE_SCHEMA,
        t.TABLE_NAME,
        p.Rows
    ORDER BY 
        TotalSpaceMB DESC
    """
    
    try:
        with mssql.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    row_dict = dict(zip(columns, row))
                    # Calculate size in appropriate unit
                    total_mb = float(row_dict['TotalSpaceMB'])
                    if total_mb >= 1024:
                        row_dict['TotalSizeFormatted'] = f"{total_mb / 1024:.2f} GB"
                    else:
                        row_dict['TotalSizeFormatted'] = f"{total_mb:.2f} MB"
                    
                    row_dict['RowCountFormatted'] = f"{int(row_dict['RowCount']):,}"
                    results.append(row_dict)
                
                return results
    except Exception as e:
        print(f"Error: {e}")
        return []

@app.route('/')
def index():
    tables = get_table_sizes()
    return render_template('index.html', tables=tables)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
