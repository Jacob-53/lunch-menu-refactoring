import streamlit as st
import requests
import lunch_menu_refactoring.constants as const
import datetime

st.set_page_config(page_title="Age Calculator", page_icon="🧮")
st.page_link("Main.py", label="Back to Main", icon="🏠")

st.sidebar.header("Age Calculator")

bday = st.date_input("생년월일을 입력하세요",min_value=datetime.date(1950,1,1))
bdayPress = st.button("조회하기")

if bdayPress:
    headers = {
        'accept': 'application/json',}
    
    response = requests.get(f'{const.API_AGE}/{bday}', headers=headers)
    if response.status_code == 200:
        data = response.json()
        st.success(data['age'])
    else:
        st.error("관리자에게 문의 하세요")
    #response.status_code (응답코드 받는 명령어 200은 성공)
    #st.json(data)
   