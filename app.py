'''
    MAIN LOGIN PAGE
'''


## MODULE IMPORTS ##
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


## STREAMLIT PAGE STYLESHEET ##
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


## STREAMLIT PAGE DEFINITION ##
# 로그인 동작애 관련한 함수
def login():
    st.title("관리자 로그인")
    username = st.text_input("관리자 번호")
    password = st.text_input("비밀번호", type = "password")
    login_button = st.button("로그인")

    if login_button:
        if username == "admin" and password == "1234":
            st.success(f"환영합니다 {username} 님!")
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error("로그인 실패! 관리자 번호와 비밀번호를 확인하세요.")


# 로그인 했을떄 동작하는 함수 ##
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        st.switch_page('pages/cctv.py')

    else:
        login()


if __name__ == "__main__":
    main()  