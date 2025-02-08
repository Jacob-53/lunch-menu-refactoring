import streamlit as st
from  lunch_menu_refactoring.db import get_connection, insert_menu, select_table, menu_plot, date_menu

st.set_page_config(page_title="Analysis", page_icon = "🎢 ",layout="wide")
st.page_link("Main.py", label="Back to Main", icon="🏠")

st.subheader("요일별 인기메뉴 Top 3")

op_date=['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

dat = st.selectbox("조회 할 요일을 선택하세요", op_date, index=None, placeholder="조회 할 요일을 선택하세요")

isPressed = st.button("조회하기")

top_menu_date = date_menu(dat)

if isPressed:
    if isinstance(top_menu_date, str):
        st.warning("해당 일의 데이터가 없습니다")
    elif top_menu_date.empty:
        st.error("해당 일의 데이터가 없습니다")
    else:
        st.table(top_menu_date)
