import streamlit as st
from lunch_menu.db import get_connection, insert_menu, select_table, menu_plot


st.subheader("Result check")
#query = "select menu_name as menu,member_id as ename,dt from lunch_menu order by dt desc"
select_df= select_table()
select_df #check chart

gdf=select_df.groupby('ename')['menu'].count().reset_index()
gdf

menu_plot()
