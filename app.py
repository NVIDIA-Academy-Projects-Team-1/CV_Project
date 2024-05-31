import streamlit as st
import numpy as np
import pandas as pd
import torch as nn          ## 텐서플로우 쓰면 사용 X
import tensorflow as tf     ## 파이토치 쓰면 사용 X
import time
from datetime import datetime

data = np.array([[1, 2, 3, 4, 5, 6, 7, 8]])
index = ['2024.05.31']
columns = ['폭행','실신','기물파손','절도','주취','이동상인','몰카','자전거 승차']

## 현시간 출력용 데이터 구성
today = datetime.now()

## 이상행동 보고용 빈 데이타프레임 구성
empty_df = pd.DataFrame(data=data, index=index, columns=columns)
df_test = pd.DataFrame(np.random.rand(10, 5) * 9 + 1, columns=("이상 행동 %d" % i for i in range(5)))

## 비디오 출력용 테스트 데이터 구성
video_test = open('test.mp4','rb')
video_bytes = video_test.read()


## 화면 중앙이 아닌 전체에서 보이게 설정
st.set_page_config(layout="wide")

## 제일 윗단 header 바 부분
st.header('지하철 객차 내에 :red[이상행동] 탐색기',divider='rainbow')
unsafe_allow_html=True

## 사이드에서 입력 및 여러가지 동작 - 1.지하철 호선 선택해서 맟춤 영상 재생
st.sidebar.title('Settings')



## section을 3개로 나누어서 3:1:5 비율로 구성
section1, section2, section3 = st.columns([3,0.5,5])

with section1:
    st.header('확인중인 영상')
    video_container = st.container(border=True)
    with video_container:
        st.video(video_bytes,
                '''
                <style>
                .video-container {
                    width: 90%;
                    height: auto;
                    margin: 0 auto;
                }
                </style>
                '''
            )

with section2:
    pass

with section3:
    st.header('확인된 이상행동')
    graph_container = st.container(border=True)
    with graph_container:
        st.subheader(f'현재 시간 : {today}')
        st.write(' ')
        st.dataframe(empty_df)
        st.bar_chart(empty_df)       ## graph form

