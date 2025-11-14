import streamlit as st
import mssql_python as mssql
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SQL Server Index Usage Stats",
    page_icon="📊",
    layout="wide"
)

@st.cache_resource
def get_connection():
    """Create and cache database connection"""
    connection_string = os.getenv('MSSQL')
    if not connection_string:
        st.error("MSSQL connection string not found in .env file")
        return None
    
    try:
        conn = mssql.connect(connection_string)
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

def get_index_usage_stats(conn, top_n=100):
    """Query sys.dm_db_index_usage_stats"""
    query = f"""
    SELECT TOP {top_n}
        DB_NAME(ius.database_id) AS DatabaseName,
        OBJECT_SCHEMA_NAME(ius.object_id, ius.database_id) AS SchemaName,
        OBJECT_NAME(ius.object_id, ius.database_id) AS TableName,
        i.name AS IndexName,
        i.type_desc AS IndexType,
        ius.user_seeks AS UserSeeks,
        ius.user_scans AS UserScans,
        ius.user_lookups AS UserLookups,
        ius.user_updates AS UserUpdates,
        ius.last_user_seek AS LastUserSeek,
        ius.last_user_scan AS LastUserScan,
        ius.last_user_lookup AS LastUserLookup,
        ius.last_user_update AS LastUserUpdate,
        ius.system_seeks AS SystemSeeks,
        ius.system_scans AS SystemScans,
        ius.system_lookups AS SystemLookups,
        ius.system_updates AS SystemUpdates
    FROM sys.dm_db_index_usage_stats AS ius
    INNER JOIN sys.indexes AS i
        ON ius.object_id = i.object_id
        AND ius.index_id = i.index_id
    WHERE ius.database_id = DB_ID()
        AND OBJECTPROPERTY(ius.object_id, 'IsUserTable') = 1
    ORDER BY (ius.user_seeks + ius.user_scans + ius.user_lookups) DESC
    """
    
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None

def main():
    st.title("📊 SQL Server Index Usage Statistics")
    st.markdown("View and analyze index usage statistics from `sys.dm_db_index_usage_stats`")
    
    # Sidebar controls
    st.sidebar.header("Settings")
    top_n = st.sidebar.slider("Number of records to display", 10, 500, 100, 10)
    auto_refresh = st.sidebar.checkbox("Auto-refresh", False)
    
    if auto_refresh:
        refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 5, 60, 10)
    
    # Get database connection
    conn = get_connection()
    
    if conn is None:
        st.stop()
    
    # Add refresh button
    if st.sidebar.button("🔄 Refresh Data") or auto_refresh:
        st.cache_resource.clear()
    
    # Fetch data
    with st.spinner("Fetching index usage statistics..."):
        df = get_index_usage_stats(conn, top_n)
    
    if df is not None and not df.empty:
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Indexes", len(df))
        
        with col2:
            total_seeks = df['UserSeeks'].sum()
            st.metric("Total User Seeks", f"{total_seeks:,}")
        
        with col3:
            total_scans = df['UserScans'].sum()
            st.metric("Total User Scans", f"{total_scans:,}")
        
        with col4:
            total_updates = df['UserUpdates'].sum()
            st.metric("Total User Updates", f"{total_updates:,}")
        
        # Add filter options
        st.subheader("Filters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            schemas = ['All'] + sorted(df['SchemaName'].dropna().unique().tolist())
            selected_schema = st.selectbox("Schema", schemas)
        
        with col2:
            tables = ['All'] + sorted(df['TableName'].dropna().unique().tolist())
            selected_table = st.selectbox("Table", tables)
        
        with col3:
            index_types = ['All'] + sorted(df['IndexType'].dropna().unique().tolist())
            selected_type = st.selectbox("Index Type", index_types)
        
        # Apply filters
        filtered_df = df.copy()
        
        if selected_schema != 'All':
            filtered_df = filtered_df[filtered_df['SchemaName'] == selected_schema]
        
        if selected_table != 'All':
            filtered_df = filtered_df[filtered_df['TableName'] == selected_table]
        
        if selected_type != 'All':
            filtered_df = filtered_df[filtered_df['IndexType'] == selected_type]
        
        # Display data
        st.subheader(f"Index Usage Statistics ({len(filtered_df)} records)")
        
        # Add read/write ratio column
        filtered_df['TotalReads'] = (
            filtered_df['UserSeeks'] + 
            filtered_df['UserScans'] + 
            filtered_df['UserLookups']
        )
        
        filtered_df['ReadWriteRatio'] = filtered_df.apply(
            lambda row: round(row['TotalReads'] / row['UserUpdates'], 2) 
            if row['UserUpdates'] > 0 else float('inf'),
            axis=1
        )
        
        # Display dataframe with formatting
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "UserSeeks": st.column_config.NumberColumn(format="%d"),
                "UserScans": st.column_config.NumberColumn(format="%d"),
                "UserLookups": st.column_config.NumberColumn(format="%d"),
                "UserUpdates": st.column_config.NumberColumn(format="%d"),
                "TotalReads": st.column_config.NumberColumn(format="%d"),
                "ReadWriteRatio": st.column_config.NumberColumn(format="%.2f"),
                "LastUserSeek": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm:ss"),
                "LastUserScan": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm:ss"),
                "LastUserLookup": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm:ss"),
                "LastUserUpdate": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm:ss"),
            }
        )
        
        # Add charts
        st.subheader("Visualizations")
        
        tab1, tab2, tab3 = st.tabs(["Top Usage by Table", "Index Type Distribution", "Read vs Write"])
        
        with tab1:
            # Group by table and sum operations
            table_stats = filtered_df.groupby('TableName').agg({
                'UserSeeks': 'sum',
                'UserScans': 'sum',
                'UserLookups': 'sum',
                'UserUpdates': 'sum'
            }).reset_index()
            
            table_stats['TotalOperations'] = (
                table_stats['UserSeeks'] + 
                table_stats['UserScans'] + 
                table_stats['UserLookups'] + 
                table_stats['UserUpdates']
            )
            
            table_stats = table_stats.nlargest(10, 'TotalOperations')
            
            st.bar_chart(
                table_stats.set_index('TableName')[['UserSeeks', 'UserScans', 'UserLookups', 'UserUpdates']]
            )
        
        with tab2:
            index_type_counts = filtered_df['IndexType'].value_counts()
            st.bar_chart(index_type_counts)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    "Total Read Operations",
                    f"{filtered_df['TotalReads'].sum():,}",
                    help="UserSeeks + UserScans + UserLookups"
                )
            
            with col2:
                st.metric(
                    "Total Write Operations",
                    f"{filtered_df['UserUpdates'].sum():,}",
                    help="UserUpdates"
                )
            
            # Create comparison chart
            read_write_data = pd.DataFrame({
                'Operation Type': ['Reads', 'Writes'],
                'Count': [
                    filtered_df['TotalReads'].sum(),
                    filtered_df['UserUpdates'].sum()
                ]
            })
            
            st.bar_chart(read_write_data.set_index('Operation Type'))
        
    elif df is not None:
        st.warning("No data found. The table might not have any index usage statistics yet.")
    
    # Auto-refresh logic
    if auto_refresh:
        import time
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()
