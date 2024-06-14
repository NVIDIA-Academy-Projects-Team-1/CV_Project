'''
    STATISTICS PAGE
'''


## MODULE IMPORTS ## 
import streamlit as st
import datetime 
import pandas as pd
import altair as alt
import time 
import cv2
import sys

from threading import Thread
from ultralytics import YOLOv10
from collections import defaultdict
from streamlit_webrtc import webrtc_streamer


## STREAMLIT PAGE STYLESHEET ##
st.set_page_config(layout = 'wide',initial_sidebar_state = 'collapsed')

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """
, unsafe_allow_html = True)

st.markdown(
    """
    <style>
        [data-testid="collapsedControl"]{
            display: none
        }
    </style>
    """
, unsafe_allow_html = True)


## GLOBAL FIELD ##
label_count1 = st.session_state.get('label_count1', {})
label_count2 = st.session_state.get('label_count2', {})
label_count3 = st.session_state.get('label_count3', {})

## STREAMLIT PAGE DEFINITION ##
def render_chart(label_counts):
    df = pd.DataFrame(list(label_counts.items()), columns=['종류', '횟수'])
    st.dataframe(df, hide_index = True)
    chart = alt.Chart(df).mark_bar().encode(
        x = alt.X('종류:N', axis=alt.Axis(labelAngle=0)),
        y = alt.Y('횟수:Q', scale=alt.Scale(domain=[0,5]))
    ).properties()
    st.altair_chart(chart, use_container_width=True)


st.header('CCTV 기반 감지된 이상현상',divider = 'rainbow')
with st.container(border = True):
    sec1, sec2, sec3 = st.columns([3, 3, 3])
    with sec1:
        st.write('첫번쨰 CCTV')
        render_chart(label_count1)
    with sec2:
        st.write('두번쨰 CCTV')
        render_chart(label_count2)
    with sec3:
        st.write('세번쨰 CCTV')
        render_chart(label_count3)

# 버튼 눌렀을시 영상 출력 화면으로 돌아가기
if st.button('CCTV로 돌아가기'):
    st.session_state.clear()
    st.switch_page('pages/cctv.py')