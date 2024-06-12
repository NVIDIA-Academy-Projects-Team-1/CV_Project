import streamlit as st
import time
import av
from ultralytics import YOLOv10
from collections import defaultdict
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, VideoProcessorBase

# Streamlit 페이지 설정
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

# 사이드바 숨기기
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True
)

# collapse control 숨기기
st.markdown(
    """
    <style>
        [data-testid="collapsedControl"]{
            display: none
        }
    </style>
    """, unsafe_allow_html=True
)

# YOLO 객체 감지 변환기 정의
class YOLOVideoTransformer(VideoProcessorBase):
    def __init__(self):
        self.model = YOLOv10('epoch_73_best.pt')
        self.label_counts = defaultdict(int)
        self.start_time = time.time()

    # def recv(self, frame):
    #     img = frame.to_ndarray(format="rgb")
    #     results = self.model.predict(source=img, show=False)
    #     annotated_frame = results[0].plot()  # Annotate the frame

    #     return annotated_frame

    def recv(self, frame):
        img = frame.to_ndarray(format="rgb48")
        results = self.model.predict(source=img, show=False)
        annotated_frame = results[0].plot()  # Annotate the frame

        return annotated_frame
    
    
model = YOLOv10('epoch_73_best.pt')

def video_frame_callback(frame):
    img = frame.to_ndarray(format="rgb24")
    results = model.predict(source=img, show=False)
    annotated_frame = results[0].plot()  # Annotate the frame

    # flipped = img[::-1,:,:]
    return av.VideoFrame.from_ndarray(annotated_frame, format="rgb24")


# 웹캠 스트리머 실행
st.write('웹캠 테스트')
webrtc_ctx = webrtc_streamer(
    key="example",
    # video_processor_factory=YOLOVideoTransformer,
    video_frame_callback = video_frame_callback,
    # async_processing = False
)

# 버튼을 눌렀을 때 페이지 전환
if st.button('CCTV로 돌아가기'):
    st.switch_page('pages/cctv.py')
