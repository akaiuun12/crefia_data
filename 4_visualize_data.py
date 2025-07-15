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

# %% 0. Title
st.title('여신금융협회 자료 분석 - 카드사별 실적')


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
df_chart['기준년월'] = df_chart['기준년월'].astype(str)

# Add period selection component
periods = sorted(df_chart['기준년월'].unique())
default_period = [periods[0], periods[-1]] if len(periods) > 1 else periods
selected_period = st.select_slider(
    '기간 선택 (기준년월)',
    options=periods,
    value=default_period
)

# Filter data by selected period
if isinstance(selected_period, list) or isinstance(selected_period, tuple):
    start_period, end_period = selected_period
else:
    start_period = end_period = selected_period

df_chart_period = df_chart[
    (df_chart['기준년월'] >= start_period) & (df_chart['기준년월'] <= end_period)
]

# Build color scale for Altair using CI_color
color_scale = alt.Scale(domain=list(CI_color.keys()), range=list(CI_color.values()))

chart = alt.Chart(df_chart_period).mark_line(point=True).encode(
    x=alt.X('기준년월:N', title='기준년월', sort=periods),
    y=alt.Y('value:Q', title='전체회원수'),
    color=alt.Color('구분:N', scale=color_scale, title='카드사'),
)
st.altair_chart(chart, use_container_width=True)

st.dataframe(df_mbrs_psn_crd.pivot(
    index='기준년월', columns='구분', values='value'))

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

st.subheader('이용회원수 (신용카드 - 개인, 활동회원수)')

# Prepare the data for Altair
df_active_chart = df_active_users.copy()
df_active_chart['기준년월'] = df_active_chart['기준년월'].astype(str)

# Add period selection component
active_periods = sorted(df_active_chart['기준년월'].unique())
default_active_period = [active_periods[0], active_periods[-1]] if len(active_periods) > 1 else active_periods
selected_active_period = st.select_slider(
    '기간 선택 (기준년월, 이용회원수)',
    options=active_periods,
    value=default_active_period
)

# Filter data by selected period
if isinstance(selected_active_period, list) or isinstance(selected_active_period, tuple):
    start_active_period, end_active_period = selected_active_period
else:
    start_active_period = end_active_period = selected_active_period

df_active_chart_period = df_active_chart[
    (df_active_chart['기준년월'] >= start_active_period) & (df_active_chart['기준년월'] <= end_active_period)
]

# Build color scale for Altair using CI_color
color_scale_active = alt.Scale(domain=list(CI_color.keys()), range=list(CI_color.values()))

active_chart = alt.Chart(df_active_chart_period).mark_line(point=True).encode(
    x=alt.X('기준년월:N', title='기준년월', sort=active_periods),
    y=alt.Y('value:Q', title='이용회원수'),
    color=alt.Color('구분:N', scale=color_scale_active, title='카드사'),
)
st.altair_chart(active_chart, use_container_width=True)

st.dataframe(df_active_users.pivot(
    index='기준년월', columns='구분', values='value'))

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

df_new_chart = df_new_users.copy()
df_new_chart['기준년월'] = df_new_chart['기준년월'].astype(str)

new_periods = sorted(df_new_chart['기준년월'].unique())
default_new_period = [new_periods[0], new_periods[-1]] if len(new_periods) > 1 else new_periods
selected_new_period = st.select_slider(
    '기간 선택 (기준년월, 신규회원수)',
    options=new_periods,
    value=default_new_period
)

if isinstance(selected_new_period, list) or isinstance(selected_new_period, tuple):
    start_new_period, end_new_period = selected_new_period
else:
    start_new_period = end_new_period = selected_new_period

df_new_chart_period = df_new_chart[
    (df_new_chart['기준년월'] >= start_new_period) & (df_new_chart['기준년월'] <= end_new_period)
]

color_scale_new = alt.Scale(domain=list(CI_color.keys()), range=list(CI_color.values()))

new_chart = alt.Chart(df_new_chart_period).mark_line(point=True).encode(
    x=alt.X('기준년월:N', title='기준년월', sort=new_periods),
    y=alt.Y('value:Q', title='신규회원수'),
    color=alt.Color('구분:N', scale=color_scale_new, title='카드사'),
)
st.altair_chart(new_chart, use_container_width=True)

st.dataframe(df_new_users.pivot(
    index='기준년월', columns='구분', values='value'))

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

df_cancel_chart = df_cancel_users.copy()
df_cancel_chart['기준년월'] = df_cancel_chart['기준년월'].astype(str)

cancel_periods = sorted(df_cancel_chart['기준년월'].unique())
default_cancel_period = [cancel_periods[0], cancel_periods[-1]] if len(cancel_periods) > 1 else cancel_periods
selected_cancel_period = st.select_slider(
    '기간 선택 (기준년월, 해지회원수)',
    options=cancel_periods,
    value=default_cancel_period
)

if isinstance(selected_cancel_period, list) or isinstance(selected_cancel_period, tuple):
    start_cancel_period, end_cancel_period = selected_cancel_period
else:
    start_cancel_period = end_cancel_period = selected_cancel_period

df_cancel_chart_period = df_cancel_chart[
    (df_cancel_chart['기준년월'] >= start_cancel_period) & (df_cancel_chart['기준년월'] <= end_cancel_period)
]

color_scale_cancel = alt.Scale(domain=list(CI_color.keys()), range=list(CI_color.values()))

cancel_chart = alt.Chart(df_cancel_chart_period).mark_line(point=True).encode(
    x=alt.X('기준년월:N', title='기준년월', sort=cancel_periods),
    y=alt.Y('value:Q', title='해지회원수'),
    color=alt.Color('구분:N', scale=color_scale_cancel, title='카드사'),
)
st.altair_chart(cancel_chart, use_container_width=True)

st.dataframe(df_cancel_users.pivot(
    index='기준년월', columns='구분', values='value'))


# %% 3. Finance
