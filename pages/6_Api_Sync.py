import streamlit as st
from  lunch_menu_refactoring.db import api_sync,check_api

st.set_page_config(page_title="Api Sync", page_icon = "🔄")
st.page_link("Main.py", label="Back to Main", icon="🏠")
st.title("🔄 API Sync")
st.sidebar.header("🔄 API Sync")
syncPress = st.button("Sync")
if syncPress:
    with st.spinner("⌛ 조회 중 입니다",show_time=True):
        api_sync()
    
st.subheader("🚥 Api Status")
apistatusPres= st.button("Api Status")
if apistatusPres:
    with st.spinner("⌛ 조회 중 입니다",show_time=True):
        status_results = check_api()
        for status in status_results:
            st.write(status)