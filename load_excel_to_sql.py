import pandas as pd
import os
from sqlalchemy import create_engine

# Path to the data folder
data_folder = 'data'

# SQLite database path
db_path = 'my_database.db'

# Create engine
engine = create_engine(f"sqlite:///{db_path}")

def load_excel_to_sql(file_path, table_name):
    """Load Excel file into SQLite table."""
    try:
        data = pd.read_excel(file_path)
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        data.dropna(subset=['Date'], inplace=True)  # Drop invalid dates
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
        print(data.info())
        data.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Loaded {file_path} into table '{table_name}'")
        print(f"Columns: {list(data.columns)}")
        print(f"Number of rows: {len(data)}")
    except Exception as e:
        print(f"Error loading {file_path}: {e}")

def quering_sql(state):
    # tables = ['accountWise_Billable_forecasted', 'accountWise_Billable']
    # for file_name in os.listdir(data_folder):
    #     if file_name.endswith('.xlsx'):
    #         file_path = os.path.join(data_folder, file_name)
    #         table_name = file_name.replace('.xlsx', '')
    #         load_excel_to_sql(file_path, table_name)
    query=state['sql_query']
#     query="""SELECT Date, Europe
# FROM accountWise_Billable
# WHERE Date >= date('now', '-30 days')
# ORDER BY Date"""
    result = pd.read_sql_query(query, con=engine)
    # print(pd.read_sql_query("SELECT MIN(Date), MAX(Date) FROM accountWise_Billable;", con=engine)
    print(result)
    state['sql_result']=result
    print("result sql",state['sql_result'])
    return state




# def query_table(table_name, query):
#     """Execute a query on the table."""
#     try:
#         result = pd.read_sql_query(query, con=engine)
#         print(f"\nQuery result for table '{table_name}':")
#         print(result.head())  # Print first 5 rows
#     except Exception as e:
#         print(f"Error querying {table_name}: {e}")

# Load all Excel files in data folder


# # Sample queries for each table


# for table in tables:
#     # Sample query: Select all columns, limit to 5 rows
#     query = f"SELECT * FROM {table} LIMIT 5"
#     query_table(table, query)

#     # If table has 'Date' column, add a date-based query like in localsql.py
#     # But since we don't know columns, we'll assume based on existing
#     if table in ['accountWise_Billable_forecasted', 'accountWise_Billable']:
#         query = f"SELECT Date, Europe FROM {table} WHERE Date >= date('now') AND Date <= date('now', '+30 days') ORDER BY Date LIMIT 5"
#         query_table(table, query)

