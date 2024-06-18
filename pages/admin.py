import streamlit as st
import pandas as pd
import altair as alt
from google.cloud import firestore
import io
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference

st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <style>
        [data-testid="collapsedControl"]{
            display: none
        }
    </style>
    """, unsafe_allow_html=True)

db = firestore.Client.from_service_account_json(".streamlit/firebase_key.json")

label_counts = {}
docs = db.collection("trains").get()
for doc in docs:
    data = doc.to_dict()
    for key, value in data.items():
        if key in label_counts:
            label_counts[key] += value
        else:
            label_counts[key] = value

class_name = list(label_counts.keys())
test_value = list(label_counts.values())

new_class_names = {
    'assault': '폭행',
    'fainting': '실신',
    'property_damage': '기물파손',
    'theft': '도둑',
    'merchant': '잡상인',
    'spy_camera': '몰래카메라'
}
class_names_kor = [new_class_names.get(name, name) for name in class_name]

def render_chart(label_counts):
    df = pd.DataFrame({'객체': class_names_kor, '총 탐지수': label_counts})
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('객체:N', axis=alt.Axis(labelAngle=0, title='객체')),
        y=alt.Y('총 탐지수:Q', axis=alt.Axis(title='총 탐지수'), scale=alt.Scale(domain=[0, max(label_counts) + 1]))
    ).properties(
        width=alt.Step(40)
    )
    
    # df_style = df.style.set_properties(**{'text-align': 'center'})

    s1 = dict(selector='th', props=[('text-align', 'center')])
    s2 = dict(selector='td', props=[('text-align', 'center')])
    table = df.style.set_table_styles([s1,s2]).hide(axis=0).to_html()

    col1, col2, col3 = st.columns([2, 0.3, 10])

    with col1:
        st.write(f'{table}', unsafe_allow_html=True)

    with col2:
        pass

    with col3:
        st.altair_chart(chart, use_container_width=True)

st.header('CCTV 기반 감지된 이상현상', divider='rainbow')

with st.container(border=True):
    render_chart(test_value)

# 저장 버튼 클릭 시 실행되는 동작
if st.button('저장'):
    # 데이터프레임 생성
    df = pd.DataFrame({'라벨 종류': class_names_kor, '횟수': test_value})
    
    # 엑셀 파일 생성
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

        # 엑셀 워크북과 워크시트 가져오기
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # 차트 생성 및 설정
        chart = BarChart()
        chart.title = '라벨별 횟수'
        data = Reference(worksheet, min_col=2, min_row=1, max_row=len(df))
        categories = Reference(worksheet, min_col=1, min_row=2, max_row=len(df))
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(categories)

        # 엑셀 워크시트에 차트 삽입
        worksheet.add_chart(chart, 'E2')

    # 파일 포인터를 처음으로 되돌리고 다운로드 버튼 생성
    output.seek(0)
    st.download_button(label="엑셀 파일 다운로드", data=output, file_name='result.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
