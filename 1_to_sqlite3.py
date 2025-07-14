# %%
"""
preprocess_data.py
Handles merging, cleaning, transforming, and saving the processed data to the master table.
"""

import os
import pandas as pd
import sqlite3

csv_folder = 'csv'
db_filename = 'master.db'
table_name = 'master_table'

# Get all CSV files in the folder
csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

# Read and concatenate all CSV files into a single DataFrame
df_list = []
for file in csv_files:
    file_path = os.path.join(csv_folder, file)
    df = pd.read_csv(file_path)
    df_list.append(df)

if df_list:
    master_df = pd.concat(df_list, ignore_index=True)
else:
    master_df = pd.DataFrame()  # Empty DataFrame if no CSVs found

# Save the DataFrame to a SQLite database
with sqlite3.connect(db_filename) as conn:
    master_df.to_sql(table_name, conn, if_exists='replace', index=False)
