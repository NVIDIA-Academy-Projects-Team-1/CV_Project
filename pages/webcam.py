'''
    WEBCAM DETECTION
'''


## MODULE IMPORTS ##
import streamlit as st
import time
import av

from ultralytics import YOLOv10
from streamlit_webrtc import webrtc_streamer


## AUTHORIZATION CHECK ##
# try:
#     if st.session_state['logged_in_car'] == False:
#         st.switch_page('app.py')
# except:
#     st.switch_page('app.py')


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


## GLOBAL FIELD ##
model = YOLOv10('epoch_73_best.pt')


def video_frame_callback(frame):
    img = frame.to_ndarray(format = "rgb24")
    # result = model.predict(source = img, show = False, classes = [0, 1, 2, 3, 4, 5], device = 0)
    result = model.predict(source = img, show = False, classes = [0, 1, 2, 3, 4, 5])

    annotated_frame = result[0].plot()
    return av.VideoFrame.from_ndarray(annotated_frame, format = "rgb24")


## STREAMLIT PAGE DEFINITION ##
# 웹캠 스트리머 실행
st.write('웹캠 테스트')
webrtc_ctx = webrtc_streamer(
    key="example",
    video_frame_callback = video_frame_callback,
    media_stream_constraints = {
        "video": {
            "width" : 3840,
            "height" : 2160
        }
    }
)

# 버튼을 눌렀을 때 페이지 전환
if st.button('CCTV 확인'):
    st.switch_page('pages/cctv.py')
