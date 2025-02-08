import streamlit as st
from  lunch_menu_refactoring.db import get_connection, insert_menu, bulk_insert

st.set_page_config(page_title="bulk insert", page_icon="💾")

st.page_link("Main.py", label="Back to Main", icon="🏠")

st.title("bulk insert")
st.markdown("# 기존데이터 한방에 옮기기")
st.sidebar.header("bulk insert")

onePress = st.button("한방에 인서트")
if onePress:
    bulk_insert()
