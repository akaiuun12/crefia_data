# %% 
import os
import numpy as np 
import pandas as pd
import streamlit as st

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

# %% Streamlit detailed visualization
st.title('카드이용실적 마스터테이블 상세 시각화')

# Column selection
columns = st.multiselect('표시할 컬럼 선택', list(df_master.columns), default=list(df_master.columns))
df_view = pd.DataFrame(df_master[columns])

# Filtering by 기준년월
if isinstance(df_view, pd.DataFrame) and '기준년월' in df_view.columns:
    months = df_view['기준년월'].dropna().unique().tolist()
    selected_months = st.multiselect('기준년월 필터', months, default=months)
    df_view = df_view[df_view['기준년월'].isin(selected_months)]

# Filtering by 대분류
if isinstance(df_view, pd.DataFrame) and '대분류' in df_view.columns:
    categories = df_view['대분류'].dropna().unique().tolist()
    selected_categories = st.multiselect('대분류 필터', categories, default=categories)
    df_view = df_view[df_view['대분류'].isin(selected_categories)]

# Show dataframe
st.subheader('데이터 미리보기')
st.dataframe(df_view)

# Summary statistics
st.subheader('요약 통계')
st.write(df_view.describe(include='all'))

# Grouping and aggregation
if st.checkbox('그룹별 합계/평균 보기'):
    groupable_cols = []
    for col in df_view.select_dtypes(include=['object', 'category']).columns:
        try:
            if pd.Series(df_view[col]).nunique() < len(df_view) // 2:
                groupable_cols.append(col)
        except Exception:
            continue
    if groupable_cols:
        group_col = st.selectbox('그룹핑할 컬럼 선택', groupable_cols)
        agg_func = st.selectbox('집계 함수 선택', ['sum', 'mean'])
        if agg_func == 'sum':
            st.write(df_view.groupby(group_col).sum(numeric_only=True))
        else:
            st.write(df_view.groupby(group_col).mean(numeric_only=True))

# Charting
st.subheader('차트 시각화')
chart_type = st.selectbox('차트 유형 선택', ['Line', 'Bar'])
if len(df_view) > 0:
    x_col = st.selectbox('X축 컬럼', df_view.columns, index=0)
    y_col = st.selectbox('Y축 컬럼', [col for col in df_view.columns if pd.api.types.is_numeric_dtype(df_view[col])], index=0)
    if chart_type == 'Line':
        st.line_chart(df_view.set_index(x_col)[y_col])
    else:
        st.bar_chart(df_view.set_index(x_col)[y_col])

# Download filtered data
st.download_button('필터링된 데이터 다운로드', df_view.to_csv(index=False), file_name='filtered_master.csv', mime='text/csv')


# %% 
