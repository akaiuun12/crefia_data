# %% 
"""
visualize_data.py
Loads the processed/master data and provides the Streamlit dashboard for interactive visualization.
"""
# %% 
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

import altair as alt
import streamlit as st

# DB Settings
db_filename = 'master.db'
table_name = 'master_table'

# Display Settings
plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

# Design Settings
CI_color = {
    '신한카드': '#0046FF',  # Shinhan Blue
    '현대카드': '#222222',  # 현대 블랙
    '우리카드': '#20C4F4',  # 우리 스카이 블루
    '삼성카드': '#1428A0',  # 삼성 블루
    '롯데카드': '#ED1C24',  # 롯데 레드
    '하나카드': '#1DB2A5',  # 하나 민트
    'KB국민카드': '#FFBC00', # KB Yellow Positive
}
# Build color scale for Altair using CI_color
CI_color_scale = alt.Scale(domain=list(CI_color.keys()), range=list(CI_color.values()))

# %% 0. Title
st.title('여신금융협회 자료 분석 (카드사별)')
st.divider()


# %% 1. Sales


# %% 2. Members

# ==============================================================
# 2-1. Total Members
# ==============================================================
with sqlite3.connect(db_filename) as conn:
    df_mbrs_psn_crd = pd.read_sql_query(f'''
        SELECT 기준년월, 구분, value 
          FROM master_table
         WHERE 1=1
           AND 개인법인구분 = '개인'
           AND 신용체크구분 = '신용카드'
           AND 대분류 = '회원수'
           AND 중분류 = '전체회원수'
           AND 소분류 = '합계'
           AND 구분 IN ('롯데카드', '삼성카드', '신한카드', '우리카드', 
                       '하나카드', '현대카드', 'KB국민카드')
        ''', conn)

st.subheader('전체회원수 (신용카드 - 개인)')

# Prepare the data for Altair
df_chart = df_mbrs_psn_crd.copy()

# Add period selection component
periods = sorted(df_chart['기준년월'].unique())
default_period = [periods[0], periods[-1]] if len(periods) > 1 else periods
selected_period = st.select_slider(
    '기간 선택 (기준년월)',
    options=periods,
    value=default_period,
    label_visibility='collapsed'
)

# Filter data by selected period
if isinstance(selected_period, list) or isinstance(selected_period, tuple):
    start_period, end_period = selected_period
else:
    start_period = end_period = selected_period

df_chart_period = df_chart[
    (df_chart['기준년월'] >= start_period) & (df_chart['기준년월'] <= end_period)
]

# Plot Altair Graph
highlight = alt.selection_point(fields=['구분'], bind='legend')

chart = alt.Chart(df_chart_period
    ).mark_line(
        point={'size':50}
    ).encode(
        x=alt.X(
            '기준년월:N',
            title='기준년월',
            sort=periods,
            axis=alt.Axis(labelAngle=270, labelOverlap=True)
        ),
        y=alt.Y(
            'value:Q',
            title='전체회원수',
            # Remove scale domain for autoscale
            scale=alt.Scale()
        ),
        color=alt.Color(
            '구분:N', 
            scale=CI_color_scale, 
            title=None,
            legend=alt.Legend(orient='bottom')
        ),
        opacity=alt.condition(highlight, alt.value(1), alt.value(0.1))
    ).add_params(
        highlight
    ).interactive(
        # Pan / Zoom
    ).properties(   
        # Width / Height
        height=400
    )

st.caption("ℹ️ Shift+Click legend to multi-select lines.")
st.altair_chart(chart, use_container_width=True)

st.dataframe(
    df_mbrs_psn_crd.pivot(index='기준년월', columns='구분', values='value')\
                   .sort_values(by='기준년월', ascending=False),
    height=200
    )
st.divider()


# ==============================================================
# 2-2. Active Users (활동회원수)
# ==============================================================
with sqlite3.connect(db_filename) as conn:
    df_active_users = pd.read_sql_query(f'''
        SELECT 기준년월, 구분, value 
          FROM master_table
         WHERE 1=1
           AND 개인법인구분 = '개인'
           AND 신용체크구분 = '신용카드'
           AND 대분류 = '회원수'
           AND 중분류 = '전체이용회원수'
           AND 소분류 = '합계'
           AND 구분 IN ('롯데카드', '삼성카드', '신한카드', '우리카드', 
                       '하나카드', '현대카드', 'KB국민카드')
        ''', conn)

st.subheader('이용회원수 (신용카드, 개인)')

# Prepare the data for Altair
df_active_chart = df_active_users.copy()
df_active_chart['기준년월'] = df_active_chart['기준년월'].astype(str)

# Add period selection component
active_periods = sorted(df_active_chart['기준년월'].unique())
default_active_period = [active_periods[0], active_periods[-1]] if len(active_periods) > 1 else active_periods
selected_active_period = st.select_slider(
    label='기간',
    options=active_periods,
    value=default_active_period,
    label_visibility="collapsed"
)

# Filter data by selected period
if isinstance(selected_active_period, list) or isinstance(selected_active_period, tuple):
    start_active_period, end_active_period = selected_active_period
else:
    start_active_period = end_active_period = selected_active_period
    
df_active_chart_period = df_active_chart[
    (df_active_chart['기준년월'] >= start_active_period) & (df_active_chart['기준년월'] <= end_active_period)
]

# Plot Altair chart
highlight = alt.selection_point(fields=['구분'], bind='legend')

active_chart = alt.Chart(df_active_chart_period
    ).mark_line(
        point={"size":50}
    ).encode(
        x=alt.X('기준년월:N', title='기준년월', sort=active_periods),
        y=alt.Y('value:Q', title='이용회원수'),
        color=alt.Color(
            '구분:N',
            scale=CI_color_scale,
            title=None,
            legend=alt.Legend(orient='bottom')
        ),
        opacity=alt.condition(highlight, alt.value(1), alt.value(0.1))
    ).add_params(
        highlight
    ).interactive(
        # Pan / Zoom
    ).properties(   
        # Width / Height
        height=400
    )

st.caption("ℹ️ Shift+Click legend to multi-select lines.")
st.altair_chart(active_chart, use_container_width=True)

st.dataframe(
    df_active_users.pivot(index='기준년월', columns='구분', values='value')\
                   .sort_values(by='기준년월', ascending=False),
    height=200
)
st.divider()

# ==============================================================
# 2-3. 신규회원수
# ==============================================================
with sqlite3.connect(db_filename) as conn:
    df_new_users = pd.read_sql_query(f'''
        SELECT 기준년월, 구분, value 
          FROM master_table
         WHERE 1=1
           AND 개인법인구분 = '개인'
           AND 신용체크구분 = '신용카드'
           AND 대분류 = '회원수'
           AND 중분류 = '신규회원수(월중)'
           AND 소분류 = '합계'
           AND 구분 IN ('롯데카드', '삼성카드', '신한카드', '우리카드', 
                       '하나카드', '현대카드', 'KB국민카드')
        ''', conn)

st.subheader('신규회원수 (신용카드 - 개인, 월중)')

# Prepare the data for Altair
df_new_chart = df_new_users.copy()

# Add period selection component
new_periods = sorted(df_new_chart['기준년월'].unique())
default_new_period = [new_periods[0], new_periods[-1]] if len(new_periods) > 1 else new_periods
selected_new_period = st.select_slider(
    '기간 선택 (기준년월, 신규회원수)',
    options=new_periods,
    value=default_new_period,
    label_visibility="collapsed"
)

# Filter data by selected period
if isinstance(selected_new_period, list) or isinstance(selected_new_period, tuple):
    start_new_period, end_new_period = selected_new_period
else:
    start_new_period = end_new_period = selected_new_period

df_new_chart_period = df_new_chart[
    (df_new_chart['기준년월'] >= start_new_period) & (df_new_chart['기준년월'] <= end_new_period)
]

# Plot Altair chart
highlight = alt.selection_point(fields=['구분'], bind='legend')

new_chart = alt.Chart(df_new_chart_period
    ).mark_line(
        point=True
    ).encode(
        x=alt.X('기준년월:N', title='기준년월', sort=new_periods),
        y=alt.Y('value:Q', title='신규회원수'),
        color=alt.Color(
            '구분:N',
            scale=CI_color_scale,
            title=None,
            legend=alt.Legend(orient='bottom')
        ),
        opacity=alt.condition(highlight, alt.value(1), alt.value(0.1))
    ).add_params(
        highlight
    ).interactive(
        # Pan / Zoom
    ).properties(   
        # Width / Height
        height=400
    )

st.caption("ℹ️ Shift+Click legend to multi-select lines.")
st.altair_chart(new_chart, use_container_width=True)

st.dataframe(
    df_new_users.pivot(index='기준년월', columns='구분', values='value')\
                .sort_values(by='기준년월', ascending=False),
    height=200
)
st.divider()

# ==============================================================
# 2-4. 해지회원수
# ==============================================================
with sqlite3.connect(db_filename) as conn:
    df_cancel_users = pd.read_sql_query(f'''
        SELECT 기준년월, 구분, value 
          FROM master_table
         WHERE 1=1
           AND 개인법인구분 = '개인'
           AND 신용체크구분 = '신용카드'
           AND 대분류 = '회원수'
           AND 중분류 = '해지회원수(월중)'
           AND 소분류 = '해지회원수(월중)'
           AND 구분 IN ('롯데카드', '삼성카드', '신한카드', '우리카드', 
                       '하나카드', '현대카드', 'KB국민카드')
        ''', conn)

st.subheader('해지회원수 (신용카드 - 개인, 월중)')

# Prepare the data for Altair
df_cancel_chart = df_cancel_users.copy()

# Add period selection component
cancel_periods = sorted(df_cancel_chart['기준년월'].unique())
default_cancel_period = [cancel_periods[0], cancel_periods[-1]] if len(cancel_periods) > 1 else cancel_periods
selected_cancel_period = st.select_slider(
    '기간 선택 (기준년월, 해지회원수)',
    options=cancel_periods,
    value=default_cancel_period,
    label_visibility="collapsed"
)

# Filter data by selected period
if isinstance(selected_cancel_period, list) or isinstance(selected_cancel_period, tuple):
    start_cancel_period, end_cancel_period = selected_cancel_period
else:
    start_cancel_period = end_cancel_period = selected_cancel_period

df_cancel_chart_period = df_cancel_chart[
    (df_cancel_chart['기준년월'] >= start_cancel_period) & (df_cancel_chart['기준년월'] <= end_cancel_period)
]

# Plot Altair chart
highlight = alt.selection_point(fields=['구분'], bind='legend')

cancel_chart = alt.Chart(df_cancel_chart_period
    ).mark_line(
        point={"size":50}
    ).encode(
        x=alt.X('기준년월:N', title='기준년월', sort=cancel_periods),
        y=alt.Y('value:Q', title='해지회원수'),
        color=alt.Color(
            '구분:N', 
            scale=CI_color_scale, 
            title=None,
            legend=alt.Legend(orient='bottom')
        ),
        opacity=alt.condition(highlight, alt.value(1), alt.value(0.1))
    ).add_params(
        highlight
    ).interactive(
        # Pan / Zoom
    ).properties(   
        # Width / Height
        height=400
    )
    
st.caption("ℹ️ Shift+Click legend to multi-select lines.")
st.altair_chart(cancel_chart, use_container_width=True)

st.dataframe(
    df_cancel_users.pivot(index='기준년월', columns='구분', values='value')\
                   .sort_values(by='기준년월', ascending=False),
    height=200
)
st.divider()
# %% 3. Finance
