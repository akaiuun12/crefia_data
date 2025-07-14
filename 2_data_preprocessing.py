# %% 
import pandas as pd
import sqlite3

db_filename = 'master.db'
table_name = 'master_table'

# Connect to the SQLite database and load the data into a DataFrame
with sqlite3.connect(db_filename) as conn:
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

# Now df contains the data from master.db and is ready for preprocessing
df
# %%