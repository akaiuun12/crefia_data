# %% 
"""
visualize_data.py
Loads the processed/master data and provides the Streamlit dashboard for interactive visualization.
"""
import sqlite3
import pandas as pd
import streamlit as st

db_filename = 'master.db'
table_name = 'master_table'

# Connect to the SQLite database and load the data into a DataFrame
with sqlite3.connect(db_filename) as conn:
    df_mbrs = pd.read_sql_query(f'''
        SELECT 기준년월, 구분, value 
          FROM master_table
         WHERE 1=1
           AND 신용체크구분 = '신용카드'
           AND 개인법인구분 = '개인'
           AND 대분류 = '회원수'
           AND 중분류 = '해지회원수(월중)'
           AND 소분류 = '해지회원수(월중)'
           AND 구분 IN ('롯데카드', '삼성카드', '신한카드', '우리카드', 
                       '하나카드', '현대카드', 'KB국민카드', 'NH농협카드')
           AND 구분 = '우리카드'
        ''', conn)
        
import seaborn as sns
import matplotlib.pyplot as plt

# Ensure matplotlib handles Korean (Hangul) fonts for proper display
from matplotlib import font_manager, rc

# Try to set a common Korean font (NanumGothic, Malgun Gothic, AppleGothic, etc.)
font_candidates = ['NanumGothic', 'Malgun Gothic', 'AppleGothic', '맑은 고딕', '돋움']
found_font = False
for font_name in font_candidates:
    try:
        rc('font', family=font_name)
        found_font = True
        break
    except:
        continue

# If no Korean font found, fallback to default and warn
if not found_font:
    st.warning("한글 폰트가 시스템에 없어 그래프에 한글이 깨질 수 있습니다. 'NanumGothic' 또는 'Malgun Gothic' 폰트를 설치하세요.")

# For minus sign display
plt.rcParams['axes.unicode_minus'] = False


st.title('월별 카드사별 해지회원수')
st.subheader('카드사별 월별 해지회원수 (Line Graph)')


# Optionally, sort by '기준년월' for correct plotting order
df_mbrs = df_mbrs.sort_values('기준년월')

st.dataframe(df_mbrs)

# Pivot the data for plotting
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=df_mbrs, x='기준년월', y='value', hue='구분', 
             markers='o', markersize=30, ax=ax)
ax.set_title('카드사별 월별 해지회원수')
ax.set_xlabel('기준년월')
ax.set_ylabel('해지회원수')
ax.legend(title='카드사')
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# %% 
# df_master = df_mbrs
# df_master = pd.read_csv('data/카드이용실적_마스터테이블.csv')

# # Column selection
# columns = st.multiselect('표시할 컬럼 선택', list(df_master.columns), default=list(df_master.columns))
# df_view = pd.DataFrame(df_master[columns])

# # Filtering by 기준년월
# if isinstance(df_view, pd.DataFrame) and '기준년월' in df_view.columns:
#     months = df_view['기준년월'].dropna().unique().tolist()
#     selected_months = st.multiselect('기준년월 필터', months, default=months)
#     df_view = df_view[df_view['기준년월'].isin(selected_months)]

# # Filtering by 대분류
# if isinstance(df_view, pd.DataFrame) and '대분류' in df_view.columns:
#     categories = df_view['대분류'].dropna().unique().tolist()
#     selected_categories = st.multiselect('대분류 필터', categories, default=categories)
#     df_view = df_view[df_view['대분류'].isin(selected_categories)]

# # Show dataframe
# st.subheader('데이터 미리보기')
# st.dataframe(df_view)

# # Summary statistics
# st.subheader('요약 통계')
# st.write(df_view.describe(include='all'))

# # Grouping and aggregation
# if st.checkbox('그룹별 합계/평균 보기'):
#     groupable_cols = []
#     for col in df_view.select_dtypes(include=['object', 'category']).columns:
#         try:
#             if pd.Series(df_view[col]).nunique() < len(df_view) // 2:
#                 groupable_cols.append(col)
#         except Exception:
#             continue
#     if groupable_cols:
#         group_col = st.selectbox('그룹핑할 컬럼 선택', groupable_cols)
#         agg_func = st.selectbox('집계 함수 선택', ['sum', 'mean'])
#         if agg_func == 'sum':
#             st.write(df_view.groupby(group_col).sum(numeric_only=True))
#         else:
#             st.write(df_view.groupby(group_col).mean(numeric_only=True))

# # Charting
# st.subheader('차트 시각화')
# chart_type = st.selectbox('차트 유형 선택', ['Line', 'Bar'])
# if len(df_view) > 0:
#     x_col = st.selectbox('X축 컬럼', df_view.columns, index=0)
#     y_col = st.selectbox('Y축 컬럼', [col for col in df_view.columns if pd.api.types.is_numeric_dtype(df_view[col])], index=0)
#     if chart_type == 'Line':
#         st.line_chart(df_view.set_index(x_col)[y_col])
#     else:
#         st.bar_chart(df_view.set_index(x_col)[y_col])

# # Download filtered data
# st.download_button('필터링된 데이터 다운로드', df_view.to_csv(index=False), file_name='filtered_master.csv', mime='text/csv')