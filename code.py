# %% 
import os
import numpy as np 
import pandas as pd

# Read label and master table
df_label = pd.read_csv('data/카드이용실적_구분.csv')
df_master = pd.read_csv('data/카드이용실적_마스터테이블.csv')

# Directory containing xls files
xls_dir = 'data'
xls_files = [f for f in os.listdir(xls_dir) if f.endswith('.xls')]

for xls_file in xls_files:
    label = xls_file.split('_')[-1].replace('.xls', '')
    df_xls = pd.read_excel(os.path.join(xls_dir, xls_file))

    # Replace first five columns with df_label using pd.concat
    df_xls = pd.concat([df_label, df_xls.iloc[:, 5:]], axis=1)
    
    # Add or update 기준년월 column
    df_xls['기준년월'] = label
    
    # Ensure columns match master table (reorder, fill missing if needed)
    missing_cols = [col for col in df_master.columns if col not in df_xls.columns]
    for col in missing_cols:
        df_xls[col] = None
    df_xls = df_xls[df_master.columns]
    
    # Append to master table
    df_master = pd.concat([df_master, df_xls], ignore_index=True)

# %% Save updated master table
# df_master.to_csv('data/카드이용실적_마스터테이블.csv', index=False)


# %% 
df_master