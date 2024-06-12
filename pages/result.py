import streamlit as st
import datetime 
import pandas as pd
import altair as alt
import time 
import cv2
from threading import Thread
from ultralytics import YOLOv10
from collections import defaultdict
from streamlit_webrtc import webrtc_streamer

st.set_page_config(layout='wide',initial_sidebar_state='collapsed')

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """
, unsafe_allow_html=True)

st.markdown(
    """
    <style>
        [data-testid="collapsedControl"]{
            display: none
        }
    </style>
""", unsafe_allow_html=True)

## 시간 출력하기 위한 필요 변수 설정
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
date_placeholder = st.empty()

def timezone():
    ## 현제 시간 출력하는 코드
    return date_placeholder.subheader(now)

def render_chart(label_counts):
    df = pd.DataFrame(list(label_counts.items()), columns=['Label', 'Count']) # index등 추가변형
    st.dataframe(df)
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Label:N', axis=alt.Axis(labelAngle=0)),
        y='Count:Q'
    ).properties()
    st.altair_chart(chart, use_container_width=True) 

## 영상 객체 인식 결과 출력하는 페이지
timezone()

st.header('필요한 영상 분석 결과 출력하는 위치')

sec1, sec2, sec3 = st.columns([3,3,3])
with sec1:
    st.write('Video 1 results')
    # render_chart()
with sec2:
    st.write('Video 2 results')
    # render_chart()
with sec3:
    st.write('Video 3 results')
    # render_chart()

## 버튼 눌렀을시 영상 출력 화면으로 돌아가기
if st.button('CCTV로 돌아가기'):
    st.switch_page('pages/cctv.py')
        