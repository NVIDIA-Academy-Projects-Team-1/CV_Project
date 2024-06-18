'''
    MAIN LOGIN PAGE
'''


## MODULE IMPORTS ##
import streamlit as st
import datetime 
import pandas as pd
import altair as alt

from threading import Thread
from google.cloud import firestore


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


## GLOBAL FIELDS ##
db = firestore.Client.from_service_account_json(".streamlit/firebase_key.json")


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
            st.session_state['logged_in_admin'] = True
            st.switch_page('pages/admin.py')
        
        elif username == "test" and password == "1234":
            st.success(f"환영합니다 1호차 님!")
            st.session_state['logged_in_car'] = True
            st.switch_page('pages/cctv.py')

        else:
            st.error("로그인 실패! 관리자 번호와 비밀번호를 확인하세요.")


if __name__ == "__main__":
    current_month = datetime.datetime.now().month

    if current_month != db.collection("current_date").document("date").get().get("month"):
        for doc in db.collection("trains").stream():
            fields = db.collection("trains").document(doc.id).get().to_dict()
            updated_fields = {field: 0 for field in fields}

            db.collection("trains").document(doc.id).update(updated_fields)
        db.collection("current_date").document("date").update({"month" : current_month})


    st.session_state['logged_in_admin'] = False
    st.session_state['logged_in_car'] = False

    login()