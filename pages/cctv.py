import streamlit as st
import datetime 
import pandas as pd
import altair as alt
import random
import time 
import cv2
import av
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

st.header('환영합니다. :red[admin] 님!',divider='rainbow')
st.subheader('지하철 내에 :blue[이상행동] 탐지')


with st.container(border=True):
    ## 영상 객수 추가 하고 싶음 추가 해서 밑에 집어 넣으면 됨
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader('CCTV 1')
        image1 = st.empty()
        image1.write('Loading video')

    with col2:
        st.subheader('CCTV 2')
        image2 = st.empty()
        image2.write('Loading video')

    with col3:
        st.subheader('CCTV 3')
        image3 = st.empty()
        image3.write('Loading video')


if st.button('View results'):
    st.switch_page('pages/result.py')
if st.button('Webcam'):
    st.switch_page('pages/webcam.py')


model = YOLOv10('epoch_73_best.pt')


def prediction(video_path, placeholder):
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        results = model.predict(source=frame, show=False)
        annotated_frame = results[0].plot() if results else None

        for det in result.boxes.data:
            class_index = int(det[1])  # 라벨 인덱스
            label = result.names[class_index]
            if label == 'fainting':
                fainting_detected = True

        

        placeholder.image(annotated_frame, channels='RGB', use_column_width = "auto")
        
    cap.release()

# fainting 라벨이 감지되었을 때 사운드, 팝업 창을 생성
def play_alarm():
    js_code = """
    <script src="alarm.js"></script>
    <script>
    openAlarmWindow();
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

fainting_detected = False

    

## 로그인 후 출력되는 메인 페이지
video_path1 = '실신_test_1.mp4'
video_path2 = 'aaa잡상인_test_1.mp4'
video_path3 = 'aaa폭행_test_1.mp4'

thread_1 = Thread(target = prediction, args = (video_path1, image1, ))
thread_2 = Thread(target = prediction, args = (video_path2, image2, ))
thread_3 = Thread(target = prediction, args = (video_path3, image3, ))

st.runtime.scriptrunner.script_run_context.add_script_run_ctx(thread_1)
st.runtime.scriptrunner.script_run_context.add_script_run_ctx(thread_2)
st.runtime.scriptrunner.script_run_context.add_script_run_ctx(thread_3)

thread_1.start()
thread_2.start()
thread_3.start()

thread_1.join()
thread_2.join()
thread_3.join()