'''
    ADMIN PAGE FOR NET STATISTICS 
'''


## MODULE IMPORTS ##
import streamlit as st
import pandas as pd
import altair as alt
import io
import matplotlib.pyplot as plt

from google.cloud import firestore
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from tempfile import NamedTemporaryFile
from openpyxl.drawing.spreadsheet_drawing import AnchorMarker


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
        }S
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
    'theft': '절도',
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


# 엑셀 파일 생성
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    x = 0
    for i in range(0, len(docs)):
        data = docs[i].to_dict()
        df = pd.DataFrame({'라벨 종류': class_names_kor, '횟수': data.values()})
        total_df = pd.DataFrame({'라벨 종류': class_names_kor, '횟수': test_value})
        if i == 0:
            x = 7
        else:
            x += 15
            
        df.to_excel(writer, index=False, sheet_name='Sheet1', startrow = x)

        if i + 2 == len(docs) + 1:
            total_df.to_excel(writer, index=False, sheet_name='Sheet1', startrow = 15*len(docs)+7)
        
        # 차트 생성 및 설정
        chart1 = BarChart()
        chart1.style = 10
        chart1.title = '라벨별 횟수'
        chart1.x_axis.delete = False
        chart1.y_axis.delete = False
        chart1.y_axis.majorUnit = 1

        # 엑셀 워크북과 워크시트 가져오기
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        worksheet['G1'] = '결과 보고서'
        
        ## car_1 일떄 x = 7 
        ## car_2 일떄 x = 15
        ## len(df) = 6

        data_range = len(df) + x + 1
        data = Reference(worksheet, min_col=2, min_row=x+1, max_row=data_range, max_col=2)
        categories = Reference(worksheet, min_col=1, min_row=x+2, max_row=data_range, max_col=1)
        chart1.add_data(data, titles_from_data=True)
        chart1.set_categories(categories)

        chart2 = BarChart()
        chart2.style = 10
        chart2.title = '라밸별 횟수'
        chart2.x_axis.delete = False
        chart2.y_axis.delete = False
        chart2.y_axis.majorUnit = 1

        t_data=Reference(worksheet, min_col=2, min_row=15*len(docs)+8, max_row=15*len(docs)+14)
        t_categories = Reference(worksheet,min_col=1, min_row=x+2, max_row=data_range)
        chart2.add_data(t_data,titles_from_data=True)
        chart2.set_categories(t_categories)


        # 엑셀 워크시트에 차트 삽입            
        worksheet.add_chart(chart1, f'F{x+1}')
        worksheet.add_chart(chart2,f'F{15*len(docs)+8}')

            
# 파일 포인터를 처음으로 되돌리고 다운로드 버튼 생성
output.seek(0)
st.download_button(label="저장", data=output, file_name='result.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


# 가장 마지막으로 할 스타일 : 각 데이터 표 위에 이름 달아주기, 그래프 포함