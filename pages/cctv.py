import streamlit as st
import datetime 
import pandas as pd
import altair as alt
import random
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


# 폭행 라벨이 감지되었을 때 사운드, 팝업 창을 생성
def play_alarm():
    js_code = """
    <script>
    var myWindow = window.open("", "AlarmWindow", "width=200,height=100");
    myWindow.document.write("<p style='text-align:center;'>폭행이 감지되었습니다.</p>");
    var audio = new Audio(/CV_Project/alarm-clock-short-6402.mp3);
    audio.play();
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)


def prediction(video_path, output_path, label_counts):
    model = YOLOv10('CV_Project/epoch_73_best.pt')
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    start_time = time.time()

    while cap.isOpened():
        success, frame = cap.read()
        if success:
            results = model.predict(source=frame, show=False)
            annotated_frame = results[0].plot()  # Annotate the frame

            # Frame label counts initialization
            frame_label_counts = defaultdict(int)

            # Count each detected object
            for result in results:
                for label in result.names:
                    frame_label_counts[label] += 1

            # Update label counts every second
            if time.time() - start_time >= 1:
                label_counts.clear()
                label_counts.update(frame_label_counts)
                start_time = time.time()

            # '폭력' 라벨이 감지되면 팝업 창과 사운드 재생
            if '폭행' in frame_label_counts:
                play_alarm()

            # Write the annotated frame to the output video file
            out.write(annotated_frame)
        else:
            break

    cap.release()
    out.release()

def first_predict():
    global output_path_1, label_counts_1
    video_path = 'aaaa실신_test_1.mp4'
    output_path_1 = 'output_1.mp4'
    label_counts_1 = defaultdict(int)
    prediction(video_path, output_path_1, label_counts_1)

def second_predict():
    global output_path_2, label_counts_2
    video_path = 'aaaa잡상인_test_1.mp4'
    output_path_2 = 'output_2.mp4'
    label_counts_2 = defaultdict(int)
    prediction(video_path, output_path_2, label_counts_2)

def third_predict():
    global output_path_3, label_counts_3
    video_path = 'aaaa폭행_test_1.mp4'
    output_path_3 = 'output_3.mp4'
    label_counts_3 = defaultdict(int)
    prediction(video_path, output_path_3, label_counts_3)

## multi threading
def multi_threading():
    thread_1 = Thread(target=first_predict)
    thread_2 = Thread(target=second_predict)
    thread_3 = Thread(target=third_predict)

    thread_1.start()
    thread_2.start()
    thread_3.start()

    thread_1.join()
    thread_2.join()
    thread_3.join()

## 로그인 후 출력되는 메인 페이지
st.header('환영합니다. :red[admin] 님!',divider='rainbow')
st.subheader('지하철 내에 :blue[이상행동] 탐지')

multi_threading()
with st.container(border=True):
    ## 영상 객수 추가 하고 싶음 추가 해서 밑에 집어 넣으면 됨
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('CCTV 1')
    #     st.video(output_path_1, autoplay=True)
    with col2:
        st.subheader('CCTV 2')
    #     st.video(output_path_2, autoplay=True)
    with col3:
        st.subheader('CCTV 3')
    #     st.video(output_path_3, autoplay=True)


if st.button('View results'):
    st.switch_page('pages/result.py')
if st.button('Webcam'):
    st.switch_page('pages/webcam.py')