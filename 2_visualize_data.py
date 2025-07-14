"""
visualize_data.py
Loads the processed/master data and provides the Streamlit dashboard for interactive visualization.
"""

import pandas as pd
import streamlit as st

def main():
    st.title('카드이용실적 마스터테이블 상세 시각화')
    df_master = pd.read_csv('data/카드이용실적_마스터테이블.csv')

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

if __name__ == "__main__":
    main() 