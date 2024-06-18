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
from google.cloud import firestore
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

# st.markdown("""
#         <style>
#         [data-testid="stDataFrameResizable"] {
#             width: auto;
#             alignment: center;
#         }
#         </style>
#     """
# , unsafe_allow_html = True)


## GLOBAL FIELD ##
db = firestore.Client.from_service_account_json(".streamlit/firebase_key.json")
car_db_ref = db.collection("trains").document("car_1")

label_count = car_db_ref.get().to_dict()
class_name = list(label_count.keys())
test_value = list(label_count.values())

new_class_names = {'assault':'폭행', 'fainting':'실신', 'property_damage':'기물파손', 'theft':'절도', 'merchant':'잡상인', 'spy_camera':'몰래카메라'}
class_names_kor = [new_class_names.get(name, name) for name in class_name]


def render_chart(label_counts):
    df = pd.DataFrame({'객체': class_names_kor,'총 탐지수': label_counts})
    
    chart = alt.Chart(df).mark_bar().encode(
        x = alt.X('객체:N', axis = alt.Axis(labelAngle = 0)),
        y = alt.Y('총 탐지수:Q', axis = alt.Axis(title='총 탐지수'), scale = alt.Scale(domain = [0,max(label_counts) + 1]))
    ).properties(
        width = alt.Step(40)  # controls width of bar
    )

    s1 = dict(selector='th', props=[('text-align', 'center')])
    s2 = dict(selector='td', props=[('text-align', 'center')])
    table = df.style.set_table_styles([s1,s2]).hide(axis=0).to_html()     
    
    col1, col2, col3 = st.columns([2, 0.3, 10])
    
    with col1:
        st.write(f'{table}', unsafe_allow_html=True)
        # st.dataframe(df, hide_index = True)

    with col2:
        pass

    with col3:
        st.altair_chart(chart, use_container_width = True)


st.header('CCTV 기반 감지된 이상현상', divider = 'rainbow')
with st.container(border = True):
    render_chart(test_value)

# 버튼 눌렀을시 영상 출력 화면으로 돌아가기
col1, col2, col3 = st.columns([1.5, 1.5, 10])
with col1:
    if st.button('CCTV 확인', use_container_width = True):
        st.session_state.clear()
        st.switch_page('pages/cctv.py')
with col2:
    if st.button('웹캠', use_container_width = True):
        st.switch_page('pages/webcam.py')
with col3:
    pass