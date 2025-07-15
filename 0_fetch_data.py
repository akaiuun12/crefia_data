# %%
import os
import pandas as pd

data_dir = 'data'
csv_dir = 'csv'
os.makedirs(csv_dir, exist_ok=True)

# Load crefia_label.csv (now in root directory)
crefia_label_path = 'crefia_label.csv'
df_label = pd.read_csv(crefia_label_path)

# List all .xls files in the data directory
xls_files = [f for f in os.listdir(data_dir) if f.endswith('.xls')]

for xls_file in xls_files:
    xls_path = os.path.join(data_dir, xls_file)
    # Extract YYYYMM from the xls filename (assuming it's after the last underscore)
    label = xls_file.split('_')[-1].replace('.xls', '')
    crefia_csv_file = f"crefia_{label}.csv"
    crefia_csv_path = os.path.join(csv_dir, crefia_csv_file)

    # Only convert if crefia_YYYYMM.csv does not already exist
    if not os.path.exists(crefia_csv_path):
        df = pd.read_excel(xls_path)
        
        # Replace first five columns with crefia_label.csv columns using pd.concat
        df = pd.concat([df_label, df.iloc[:, 5:].apply(pd.to_numeric, errors='coerce')], axis=1)

        # Add 기준년월 column
        df.insert(0, '기준년월', label)

        # Melt the DataFrame so that all columns after the first five become rows
        df = df.melt(
            id_vars=['기준년월','신용체크구분','개인법인구분','대분류','중분류','소분류'],
            var_name='구분',
            value_name='value'
        )
        df.to_csv(crefia_csv_path, index=False)
        print(f"Converted {xls_file} to {crefia_csv_file} (first five columns replaced with crefia_label.csv)")
    else:
        print(f"{crefia_csv_file} already exists, skipping.")