# import streamlit as st
# import numpy as np
# import pandas as pd
# import torch as nn          ## 텐서플로우 쓰면 사용 X
# import tensorflow as tf     ## 파이토치 쓰면 사용 X
# import time
# from datetime import datetime

# data = np.array([[1, 2, 3, 4, 5, 6, 7, 8]])
# index = ['2024.05.31']
# columns = ['폭행','실신','기물파손','절도','주취','이동상인','몰카','자전거 승차']

# ## 현시간 출력용 데이터 구성
# today = datetime.now()

# ## 이상행동 보고용 빈 데이타프레임 구성
# empty_df = pd.DataFrame(data=data, index=index, columns=columns)
# df_test = pd.DataFrame(np.random.rand(10, 5) * 9 + 1, columns=("이상 행동 %d" % i for i in range(5)))

# ## 비디오 출력용 테스트 데이터 구성
# video_test = open('test.mp4','rb')
# video_bytes = video_test.read()


# ## 화면 중앙이 아닌 전체에서 보이게 설정
# st.set_page_config(layout="wide")

# ## 제일 윗단 header 바 부분
# st.header('지하철 객차 내에 :red[이상행동] 탐색기',divider='rainbow')
# unsafe_allow_html=True

# ## 사이드에서 입력 및 여러가지 동작 - 1.지하철 호선 선택해서 맟춤 영상 재생
# st.sidebar.title('Settings')



# ## section을 3개로 나누어서 3:1:5 비율로 구성
# section1, section2, section3 = st.columns([3,0.5,5])

# with section1:
#     st.header('확인중인 영상')
#     video_container = st.container(border=True)
#     with video_container:
#         st.video(video_bytes,
#                 '''
#                 <style>
#                 .video-container {
#                     width: 90%;
#                     height: auto;
#                     margin: 0 auto;
#                 }
#                 </style>
#                 '''
#             )

# with section2:
#     pass

# with section3:
#     st.header('확인된 이상행동')
#     graph_container = st.container(border=True)
#     with graph_container:
#         st.subheader(f'현재 시간 : {today}')
#         st.write(' ')
#         st.dataframe(empty_df)
#         st.bar_chart(empty_df)       ## graph form

#========================================================================================
## 로그인 페이지 제작 하여서 로그인시 객체인식 페이지 출력
import streamlit as st

st.set_page_config(layout='wide',initial_sidebar_state='collapsed')

## 로그인 동작애 관련한 함수
def login():
    # 페이지 제목
    st.title("관리자 로그인")

    # 사용자 입력 받기
    username = st.text_input("관리자 번호")
    password = st.text_input("비밀번호", type="password")

    # 로그인 버튼
    login_button = st.button("로그인")

    # 로그인 검증
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
        main_page()
    else:
        login()

## 로그인 후 출력되는 메인 페이지
def main_page():
    st.header('횐영합니다. :red[admin] 님!',divider='rainbow')
    st.subheader('지하철 내에 :blue[이상행동] 탐지')
    
    ## 영상 객수 추가 하고 싶음 추가 해서 밑에 집어 넣으면 됨
    col1, col2, col3 = st.columns([2,2,2])
    with col1:
        vidoe_path = './test.mp4'
        st.subheader('1번쨰 CCTV')
        st.video(vidoe_path,autoplay=True)

    with col2:
        st.subheader('2번쨰 CCTV')
        st.video(vidoe_path,autoplay=True)

    with col3:
        st.subheader('3번쨰 CCTV')
        st.video(vidoe_path,autoplay=True)

    if st.button('결과 보고'):
        st.session_state['show_response'] = True
        st.experimental_rerun()
    if 'show_response' in st.session_state and st.session_state['show_response']:
        response()

def response():
    st.title('response')


if __name__ == "__main__":
    main()  