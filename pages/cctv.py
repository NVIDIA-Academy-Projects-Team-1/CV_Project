'''
    CCTV DETECTION
'''


## MODULE IMPORTS ##
import streamlit as st
import pandas as pd
import altair as alt
import cv2
import numpy as np
import streamlit.components.v1 as components
import base64

from varname import nameof
from threading import Thread
from ultralytics import YOLOv10
from google.cloud import firestore
from google.cloud.firestore import Increment


## STREAMLIT PAGE STYLESHEET ##
st.set_page_config(layout = 'wide', initial_sidebar_state = 'collapsed')

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

st.markdown(
    """
    <style>
        #c459a123 {
            text-align: center
        }
    </style>
    """
, unsafe_allow_html = True)


## GLOBAL FIELD ##
model = YOLOv10('best.pt')
db = firestore.Client.from_service_account_json(".streamlit/firebase_key.json")
car_db_ref = db.collection("trains").document("car_1")

label_names = {
    0: "assault",
    1: "fainting",
    2: "property_damage",
    3: "theft",
    4: "merchant",
    5: "spy_camera"
}


## STREAMLIT PAGE DEFINITION ##
st.header('환영합니다. :red[admin] 님!', divider = 'rainbow')
st.subheader('영상 탐지 현황')

with st.container(border = True):
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

c1, c2, c3 = st.columns([1.5, 1.5, 10])
with c1:
    if st.button('웹캠', use_container_width = True):
        st.switch_page('pages/webcam.py')

with c2:
    if st.button('탐지 통계', use_container_width = True):
        st.switch_page('pages/result.py')

with c3:
    pass


## RUN PREDICTION ##
def prediction(video_path, placeholder, cam_num):
    cap = cv2.VideoCapture(video_path)
    assault_detected = False
    fainting_detected = False
    detections = False
    label_detected = False

    while cap.isOpened():
        ret, frame = cap.read()
        detected_labels = []
        if not ret:
            break
        
        # results = model.predict(source = frame, show = False, conf = 0.8, device = 0)
        results = model.predict(source = frame, show = False, conf = 0.8)

        annotated_frame = results[0].plot() if results else None
        label4result = results[0].boxes.cls.cpu().numpy() if results else []


        if label_detected == False:
            if cam_num == "1번 카메라":
                for label in label4result:
                    car_db_ref.update({label_names[label]: Increment(1)})

            elif cam_num == "2번 카메라":
                for label in label4result:
                    car_db_ref.update({label_names[label]: Increment(1)})

            elif cam_num == "3번 카메라":
                for label in label4result:
                    car_db_ref.update({label_names[label]: Increment(1)})
                    
            label_detected = True

        if np.isin([0, 1], results[0].boxes.cls.cpu().numpy()).any():

            if 0 in results[0].boxes.cls.cpu().numpy():
                assault_detected = True
                detected_labels.append("폭행")
            if 1 in results[0].boxes.cls.cpu().numpy():
                fainting_detected = True
                detected_labels.append("실신")

            if detections:
                placeholder.image(annotated_frame, channels='RGB', use_column_width = "auto")

            elif fainting_detected or assault_detected:
                placeholder.image(annotated_frame, channels='RGB', use_column_width = "auto")
                play_alarm(cam_num, detected_labels)

            detections = True
        else:
            placeholder.image(annotated_frame, channels='RGB', use_column_width = "auto")
        
    cap.release()


# fainting, assault 라벨이 감지되었을 때 사운드, 팝업 창을 생성
def play_alarm(cam_num, labels):
    print("play_alarm called")
    audio_file = open('alert.mp3', 'rb').read()
    js_code = f"""
        <audio autoplay src="data:audio/mp3;base64,{base64.b64encode(audio_file).decode()}" type="audio/mp3"></audio>
        <script>
            document.querySelector('audio').addEventListener('play', function() {{
                alert("{cam_num}에서 {','.join(labels)}이 감지되었습니다!");
            }})
        </script>
    """
    return components.html(js_code)

video_path1 = 'frame_4611.jpg'
video_path2 = 'frame_4243.jpg'
video_path3 = 'frame_5018.jpg'

# video_path1 = '실신_test_1.mp4'
# video_path2 = '잡상인_test_1.mp4'
# video_path3 = '폭행_test_1.mp4'

# Spawn, run detection threads
thread_1 = Thread(target = prediction, args = (video_path1, image1, "1번 카메라", ))
thread_2 = Thread(target = prediction, args = (video_path2, image2, "2번 카메라", ))
thread_3 = Thread(target = prediction, args = (video_path3, image3, "3번 카메라", ))

st.runtime.scriptrunner.script_run_context.add_script_run_ctx(thread_1)
st.runtime.scriptrunner.script_run_context.add_script_run_ctx(thread_2)
st.runtime.scriptrunner.script_run_context.add_script_run_ctx(thread_3)

thread_1.start()
thread_2.start()
thread_3.start()

thread_1.join()
thread_2.join()
thread_3.join()