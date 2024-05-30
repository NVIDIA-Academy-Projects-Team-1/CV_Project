import streamlit as st
import numpy as np
import pandas as pd
import torch as nn          ## 텐서플로우 쓰면 사용 X
import tensorflow as tf     ## 파이토치 쓰면 사용 X

# st.title('Hello World')

## 이상행동 보고용 데이타프레임 구성
df_test = pd.DataFrame(np.random.rand(10, 5) * 9 + 1, columns=("이상 행동 %d" % i for i in range(5)))
video_test = open('test.mp4','rb')
video_bytes = video_test.read()

## 제일 윗단 네비게이션 바 부분
st.header('지하철 객차 내에 :red[이상행동] 탐색기',divider='rainbow')



## 사이드에서 입력 및 여러가지 동작 - 1.지하철 호선 선택해서 맟춤 영상 재생
st.sidebar.title('Settings')

## 섹션 부분 2:3 비율로 나누어서 
section1, section2 = st.columns([2,3])

with section1:
    st.header('확인중인 영상')
    st.video(video_bytes)

with section2:
    st.header('확인된 이상행동')
    st.subheader('subheader test')
    st.write('write test')
    st.dataframe(df_test)
    st.bar_chart(df_test)