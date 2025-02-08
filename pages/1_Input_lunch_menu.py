import streamlit as st
from  lunch_menu_refactoring.db import get_connection, insert_menu, select_table, menu_plot


st.set_page_config(page_title="점심 뭐 먹었나요?", page_icon="🍱")
st.page_link("Main.py", label="Back to Main", icon="🏠")

st.title("점심 뭐 먹었나요?")
st.markdown("# Let's grab a bite and then finish this up")
st.sidebar.header("점심 뭐 먹었나요?")

members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}

st.subheader("입력")

menu_name= st.text_input("메뉴 이름", placeholder="예: 참치김밥")

member_name =  st.selectbox(
    "누가 먹었나요?",
    options=list(members.keys()),
    index=list(members.keys()).index('jacob'),placeholder="누가 먹었나요?",
)

st.write("점심 먹은 사람은",member_name)

member_id = members[member_name]

dt = st.date_input("언제 먹었나요?")

isPress = st.button("Save data")

if isPress:
    if menu_name and member_id and dt:
        if insert_menu(menu_name,member_id,dt):
           st.success(f"입력 성공")
        else:
            st.error(f"입력 실패")
    else:
        st.warning(f"모든 값을 입력하세요")
