import os
from dotenv import load_dotenv
import mssql_python as mssql
import pyarrow as pa
import pyarrow.parquet as pq

# Load environment variables
load_dotenv()

# Get connection string from environment
connection_string = os.getenv('MSSQL')

# Define the columns to export
columns = ["GrantID", "IssueDate", "Kind", "USSeriesCode", "Title"]
columns_str = ", ".join(columns)

# Define batch size
batch_size = 1000

# Connect to the database
print("Connecting to database...")
conn = mssql.connect(connection_string)
cursor = conn.cursor()

# Get the total count of rows
print("Counting rows...")
cursor.execute("SELECT COUNT(*) FROM dbo.grant_microsoft")
total_rows = cursor.fetchone()[0]
print(f"Total rows to export: {total_rows}")

# Initialize parquet writer
output_file = "grant_microsoft.parquet"
writer = None
schema = None

# Process data in batches
offset = 0
batch_num = 0

try:
    while offset < total_rows:
        print(f"Processing batch {batch_num + 1} (rows {offset} to {offset + batch_size})...")
        
        # Fetch batch using OFFSET/FETCH
        query = f"""
        SELECT {columns_str}
        FROM dbo.grant_microsoft
        ORDER BY GrantID
        OFFSET {offset} ROWS
        FETCH NEXT {batch_size} ROWS ONLY
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if not rows:
            break
        
        # Convert to PyArrow table
        data = {col: [] for col in columns}
        for row in rows:
            for i, col in enumerate(columns):
                data[col].append(row[i])
        
        # Create PyArrow table
        batch_table = pa.table(data)
        
        # Initialize writer on first batch
        if writer is None:
            schema = batch_table.schema
            writer = pq.ParquetWriter(output_file, schema)
        
        # Write batch to parquet file
        writer.write_table(batch_table)
        
        offset += batch_size
        batch_num += 1
    
    print(f"\nSuccessfully exported {total_rows} rows to {output_file}")

finally:
    # Close writer
    if writer is not None:
        writer.close()
    
    # Close database connection
    cursor.close()
    conn.close()
    print("Database connection closed.")
