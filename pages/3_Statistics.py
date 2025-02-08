import streamlit as st
from  lunch_menu_refactoring.db import get_connection, insert_menu, select_table, menu_plot

st.set_page_config(page_title="Statistics", page_icon = "🎢 ",layout="wide")
st.page_link("Main.py", label="Back to Main", icon="🏠")

st.subheader("Result check")
#query = "select menu_name as menu,member_id as ename,dt from lunch_menu order by dt desc"
select_df= select_table()
st.dataframe(select_table(),use_container_width=True) #check chart

st.subheader("Count")
gdf=select_df.groupby('ename')['menu'].count().reset_index()
st.dataframe(gdf,use_container_width=True)

st.subheader("Chart")
menu_plot()
