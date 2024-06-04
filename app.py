## 로그인 페이지 제작 하여서 로그인시 객체인식 페이지 출력
import streamlit as st
import datetime 
import pandas as pd
import altair as alt
import random
import time 
from threading import Thread

st.set_page_config(layout='wide',initial_sidebar_state='collapsed')

## 시간 출력하기 위한 필요 변수 설정
today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
date_placeholder = st.empty()

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
        if 'show_response' in st.session_state and st.session_state['show_response']:
            response()
        else:
            main_page()
    else:
        login()

## 로그인 후 출력되는 메인 페이지
def main_page():
    st.header('횐영합니다. :red[admin] 님!',divider='rainbow')
    st.subheader('지하철 내에 :blue[이상행동] 탐지')
    vidoe_paths = ['./test_1.mp4', './test_1.mp4', './test_1.mp4']

    ## 영상 객수 추가 하고 싶음 추가 해서 밑에 집어 넣으면 됨
    col1, col2, col3 = st.columns([2,2,2])
    with col1:
        st.subheader('1번쨰 CCTV')
        st.video(vidoe_paths[0],autoplay=True)

    with col2:
        st.subheader('2번쨰 CCTV')
        st.video(vidoe_paths[1],autoplay=True)

    with col3:
        st.subheader('3번쨰 CCTV')
        st.video(vidoe_paths[2],autoplay=True)

    ## 버튼 눌렀을시 결과 출력하는 화면으로 이동하기
    if st.button('결과 보고'):
        st.session_state['show_response'] = True
        st.experimental_rerun()

def timezone():
    ## 현제 시간 출력하는 코드
    return date_placeholder.subheader(today)
    
def render_chart():
    ## 데이터 출력용 테스트 데이터 프레임 생성
    numbers = random.sample(list(range(1,8)),7)
    df_test = pd.DataFrame(data=numbers,index=['폭행','실신','기물파손','절도','이동상인','몰카','자전거 승차'],columns=['Count'])
    st.dataframe(df_test)
    chart = alt.Chart(df_test.reset_index()).mark_bar().encode(x=alt.X('index:N',
                axis=alt.Axis(labelAngle=0)),y='Count:Q').properties()    ## bar chart 에서 x label 표시를 사용자중점으로 인코딩
    st.altair_chart(chart, use_container_width=True)    

## 영상 객체 인식 결과 출력하는 페이지
def response():
   
    timezone()
    
    st.header('필요한 영상 분석 결과 출력하는 위치')
    
    sec1, sec2, sec3 = st.columns([3,3,3])

    with sec1:
        st.write('1번 영상 결과')
        render_chart()
    
    with sec2:
        st.write('2번 영상 결과')
        render_chart()

    with sec3:
        st.write('3번 영상 결과')
        render_chart()

    ## 버튼 눌렀을시 영상 출력 화면으로 돌아가기
    if st.button('CCTV로 돌아가기'):
        st.session_state['show_response'] = False
        st.experimental_rerun()
    
    time.sleep(1)              ## 업데이트를 몇초 주기로 할건지 설정
    # st.experimental_rerun()

if __name__ == "__main__":
    main()  