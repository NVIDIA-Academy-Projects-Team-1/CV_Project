## 로그인 페이지 제작 하여서 로그인시 객체인식 페이지 출력
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

st.set_page_config(layout='wide',initial_sidebar_state='collapsed')

## 시간 출력하기 위한 필요 변수 설정
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
date_placeholder = st.empty()

## 로그인 동작애 관련한 함수
def login():
    st.title("관리자 로그인")
    username = st.text_input("관리자 번호")
    password = st.text_input("비밀번호", type="password")
    login_button = st.button("로그인")

    if login_button:
        if username == "admin" and password == "1234":
            st.success(f"환영합니다 {username} 님!")
            st.session_state['logged_in'] = True
            st.experimental_rerun()
        else:
            st.error("로그인 실패! 관리자 번호와 비밀번호를 확인하세요.")

## 로그인 했을떄 동작하는 함수
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        if 'show_response' in st.session_state and st.session_state['show_response']:
            response()
        else:
            main_page()
    else:
        login()

def prediction(video_path, output_path, label_counts):
    model = ''
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

            # Write the annotated frame to the output video file
            out.write(annotated_frame)
        else:
            break

    cap.release()
    out.release()

def first_predict():
    global output_path_1, label_counts_1
    video_path = 'C:/Users/shihw/OneDrive/바탕 화면/test_1.mp4'
    output_path_1 = 'output_1.mp4'
    label_counts_1 = defaultdict(int)
    prediction(video_path, output_path_1, label_counts_1)

def second_predict():
    global output_path_2, label_counts_2
    video_path = 'C:/Users/shihw/OneDrive/바탕 화면/test_1.mp4'
    output_path_2 = 'output_2.mp4'
    label_counts_2 = defaultdict(int)
    prediction(video_path, output_path_2, label_counts_2)

def third_predict():
    global output_path_3, label_counts_3
    video_path = 'C:/Users/shihw/OneDrive/바탕 화면/test_1.mp4'
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
def main_page():
    st.header('환영합니다. :red[admin] 님!',divider='rainbow')
    st.subheader('지하철 내에 :blue[이상행동] 탐지')

    multi_threading()

    ## 영상 객수 추가 하고 싶음 추가 해서 밑에 집어 넣으면 됨
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        st.subheader('CCTV 1')
        st.video(output_path_1, autoplay=True)

    with col2:
        st.subheader('CCTV 2')
        st.video(output_path_2, autoplay=True)

    with col3:
        st.subheader('CCTV 3')
        st.video(output_path_3, autoplay=True)

    if st.button('View results'):
        st.session_state['show_response'] = True

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
def response():
   
    timezone()
    
    st.header('필요한 영상 분석 결과 출력하는 위치')
    
    sec1, sec2, sec3 = st.columns([3,3,3])

    with sec1:
        st.write('Video 1 results')
        render_chart(label_counts_1)
    
    with sec2:
        st.write('Video 2 results')
        render_chart(label_counts_2)

    with sec3:
        st.write('Video 3 results')
        render_chart(label_counts_3)

    ## 버튼 눌렀을시 영상 출력 화면으로 돌아가기
    if st.button('CCTV로 돌아가기'):
        st.session_state['show_response'] = False
        
    
    time.sleep(1)              ## 업데이트를 몇초 주기로 할건지 설정
    # st.experimental_rerun()

if __name__ == "__main__":
    main()  