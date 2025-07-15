# %% 
import pandas as pd
import sqlite3

db_filename = 'master.db'
table_name = 'master_table'

# Connect to the SQLite database and load the data into a DataFrame
with sqlite3.connect(db_filename) as conn:
    df = pd.read_sql_query(f'''
    SELECT * 
      FROM {table_name}
     WHERE 1=1
       AND 구분 IN ('롯데카드', '삼성카드', '신한카드', '우리카드', 
                   '하나카드', '현대카드', 'KB국민카드', 'NH농협카드')
    ''', conn)

# %% 1. Data Segmentation
df_sales = df[df['대분류'].isin(['국내이용금액', '해외이용금액'])]
df_mbrs = df[df['대분류'] == '회원수']
df_fin = df[df['대분류'] == '금융자산']

# %% 2. Sales
print(df_sales.shape)

df_sales_psn = df_sales[df_sales['개인법인구분'] == '개인']
df_sales_co = df_sales[df_sales['개인법인구분'] == '법인']

# 3-1. 개인회원
print(df_sales_psn.shape)

# 3-2. 법인회원
print(df_sales_co.shape)


# %% 3. Members
print(df_mbrs.shape)
df_mbrs_psn = df_mbrs[df_mbrs['개인법인구분'] == '개인']
df_mbrs_co = df_mbrs[df_mbrs['개인법인구분'] == '법인']

# 3-1. 개인회원
print(df_mbrs_psn.shape)
print(df_mbrs_psn.groupby('신용체크구분').count())
df_mbrs_psn_crd = df_mbrs_psn[df_mbrs_psn['신용체크구분'] == '신용카드']
df_mbrs_psn_cnf = df_mbrs_psn[df_mbrs_psn['신용체크구분'] == '직불/체크카드']

print(df_mbrs_psn_crd[['중분류', '소분류']].value_counts())

import seaborn as sns
import matplotlib.pyplot as plt

plt.rc('font', family='NanumGothic')

# 카드사별 색상 매핑
card_colors = {
    '신한카드': '#0046FF',    # 신한 블루
    '현대카드': '#222222',    # 현대 블랙
    '우리카드': '#00B8F1',    # 우리 스카이 블루
    '삼성카드': '#1428A0',    # 삼성 블루
    '롯데카드': '#ED1C24',    # 롯데 레드
    '하나카드': '#1DB2A5',    # 하나 민트
    '씨티카드': '#005BAC',    # Citi 블루
    'NH농협카드': '#95C11F',  # 농협 옐로우-그린
}

# 전체회원수
plt.figure(figsize=(10, 5))
df_plot = df_mbrs_psn_crd[df_mbrs_psn_crd['중분류'] == '전체회원수']
# Sort by 기준년월 for proper line plotting
df_plot = df_plot.sort_values('기준년월')

# Get unique 카드사(구분) in plotting order
card_order = df_plot['구분'].unique().tolist()
# Build color list in order
palette = [card_colors.get(card, '#888888') for card in card_order]

sns.lineplot(
    data=df_plot,
    x='기준년월', y='value', hue='구분', marker='o', palette=palette, hue_order=card_order
)
plt.title('전체회원수 (신용카드-개인) 추이')
plt.xlabel('기준년월')
plt.ylabel('전체회원수')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 이용회원수
plt.figure(figsize=(10, 5))
df_plot = df_mbrs_psn_crd[df_mbrs_psn_crd['중분류'] == '전체이용회원수']
df_plot = df_plot.sort_values('기준년월')

# Get unique 카드사(구분) in plotting order
card_order = df_plot['구분'].unique().tolist()
# Build color list in order using CI color
palette = [card_colors.get(card, '#888888') for card in card_order]

sns.lineplot(
    data=df_plot,
    x='기준년월', y='value', hue='구분', marker='o', palette=palette, hue_order=card_order
)
plt.title('이용회원수 (신용카드-개인) 추이')
plt.xlabel('기준년월')
plt.ylabel('이용회원수')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 신규회원수
plt.figure(figsize=(10, 5))
df_plot = df_mbrs_psn_crd[df_mbrs_psn_crd['중분류'] == '신규회원수(월중)']
df_plot = df_plot.sort_values('기준년월')

card_order = df_plot['구분'].unique().tolist()
palette = [card_colors.get(card, '#888888') for card in card_order]

sns.lineplot(
    data=df_plot,
    x='기준년월', y='value', hue='구분', marker='o', palette=palette, hue_order=card_order
)
plt.title('신규회원수 (신용카드-개인) 추이')
plt.xlabel('기준년월')
plt.ylabel('신규회원수')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 해지회원수
plt.figure(figsize=(10, 5))
df_plot = df_mbrs_psn_crd[df_mbrs_psn_crd['중분류'] == '해지회원수(월중)']
df_plot = df_plot.sort_values('기준년월')

card_order = df_plot['구분'].unique().tolist()
palette = [card_colors.get(card, '#888888') for card in card_order]

sns.lineplot(
    data=df_plot,
    x='기준년월', y='value', hue='구분', marker='o', palette=palette, hue_order=card_order
)
plt.title('해지회원수 (신용카드-개인, 월중) 추이')
plt.xlabel('기준년월')
plt.ylabel('해지회원수(월중)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



# 3-2. 법인회원
print(df_mbrs_co.shape)
print(df_mbrs_co.groupby('신용체크구분').count())


# %% 4. Finance
print(df_fin.shape)