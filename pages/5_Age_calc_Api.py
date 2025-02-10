import streamlit as st
import requests
import json

st.set_page_config(page_title="Age Calculator", page_icon="🧮")
st.page_link("Main.py", label="Back to Main", icon="🏠")

st.sidebar.header("Age Calculator")

bday = st.date_input("생년월일을 입력하세요")
bdayPress = st.button("조회하기")

if bdayPress:
    headers = {
        'accept': 'application/json',}
    response = requests.get(f'https://acalc.jacob53.shop/api/py/ageCalculator/{bday}', headers=headers)
    data = response.json()
    st.json(data)