import streamlit as st
from lunch_menu.db import get_connection, insert_menu, chek_agents, today_agents
import time
from datetime import datetime


st.set_page_config(page_title="입력 안한 요원 찾기", page_icon="🕵")

st.title("입력 안한 요원 찾기")
st.subheader("**조회 할 날짜를 선택하세요**") 
st.sidebar.header("입력 안한 요원 찾기")

cdt = st.date_input("조회 할 날짜")
chekPress = st.button("입력 안 한 요원 누구냐?")
checkagent=chek_agents(cdt)

if chekPress:
   st.success(checkagent)


#미입력자 알림창
st.title("오늘 점심 미입력자")
st.markdown(
    """
    <style>
    .fixed-text {
        font-size: 48px;
        font-weight: bold;
        color: red;
        text-align: center;
        position: fixed;
        top: 50px;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        background-color: black;
        padding: 10px;
        z-index: 1000;
    }
    .content {
        margin-top: 150px;}
    </style>
    """,
    unsafe_allow_html=True
)

tdd = datetime.today().strftime('%Y-%m-%d')
return_text = today_agents(tdd)
display_area = st.empty()
colors = ["red", "orange", "yellow", "green", "blue", "purple"]


while True:
    for color in colors:
        display_area.markdown(
                f'<h1 style="color:{color}; text-align:center;">{return_text}</h1>',
                unsafe_allow_html=True
        )
        #st.subheader(sub_text)
        time.sleep(0.5)
