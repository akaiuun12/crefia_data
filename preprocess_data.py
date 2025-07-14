# %% 
"""
preprocess_data.py
Handles merging, cleaning, transforming, and saving the processed data to the master table.
"""

import os
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

# Save updated master table
df_master.to_csv('data/카드이용실적_마스터테이블.csv', index=False)
print("[preprocess_data.py] Master table updated.")


# %%
import pandas as pd
import os

df_master = pd.read_csv('data/카드이용실적_마스터테이블.csv')

# Ensure output directory exists
os.makedirs('csv', exist_ok=True)

# Get unique months (기준년월)
months = df_master['기준년월'].dropna().unique()

for month in months:
    df_month = df_master[df_master['기준년월'] == month]
    # Melt the dataframe for this month
    df_melted = df_month.melt(
        id_vars=['기준년월', '신용체크구분', '개인법인구분', '대분류', '중분류', '소분류'],
        value_vars=df_month.columns[5:],
        var_name='구분',
        value_name='value'
    ).fillna('금융자산')

    # Save to CSV
    out_path = f'csv/crefia_{month}.csv'
    df_melted.to_csv(out_path, index=False, encoding='utf-8-sig')
