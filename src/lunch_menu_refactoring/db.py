import streamlit as st
import pandas as pd
import psycopg
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import time
from datetime import datetime



load_dotenv()

DB_CONFIG = { 
    "dbname": os.getenv("DB_NAME"),
    "user":os.getenv("DB_USERNAME"),
    "password":os.getenv("DB_PASSWORD"),
    "host":os.getenv("DB_HOST"),
    "port":os.getenv("DB_PORT")                                         
}

def get_connection():
    return psycopg.connect(**DB_CONFIG)

# 메뉴 입력기
def insert_menu(menu_name,member_id,dt):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
                "INSERT INTO lunch_menu (menu_name,member_id,dt) VALUES (%s,%s,%s);",
                   (menu_name,member_id,dt)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        print(f"Exception : {e}")
        return False

# 확인창
def select_table():
    query="""SELECT
        lunch_menu.menu_name AS menu,
        member.name AS ename,
        lunch_menu.dt
        FROM member
        INNER JOIN lunch_menu ON member.id = lunch_menu.member_id
        ORDER BY lunch_menu.dt DESC"""

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()


    selected_df = pd.DataFrame(rows,columns=['menu','ename','dt'])
        
    return selected_df

# 메뉴 그래프
def menu_plot():
    try:
        query="""SELECT
        lunch_menu.menu_name AS menu,
        member.name AS ename,
        lunch_menu.dt
        FROM member
        INNER JOIN lunch_menu ON member.id = lunch_menu.member_id
        ORDER BY lunch_menu.dt DESC"""

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        select_df = pd.DataFrame(rows,columns=['menu','ename','dt'])
        gdf=select_df.groupby('ename')['menu'].count().reset_index()

        fig, ax = plt.subplots()
        gdf.plot(x='ename',y='menu',kind='bar',ax=ax)

        return st.pyplot(fig)
    except Exception as e:
        return "차트를 그리기에 충분한 데이터가 없습니다"

# 입력 안한 요원찾기 
def chek_agents(cdt):
    queryy = """
        select
            m.name,count(l.id) as menc
        from
            member m
        left join lunch_menu l
        on
            l.member_id = m.id and l.dt = %s
        group by
            m.id, m.name
        having
            count(l.id) = 0
        order by
            menc desc"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(queryy,(cdt,))
        rowss = cursor.fetchall()
        fdf=pd.DataFrame(rowss,columns=['name','count'])
        sunsinagents=fdf['name'].tolist()
        if len(sunsinagents) >=1:
            #st.text(",  ".join(sunsinagents))
            cursor.close()
            conn.close()
            return ",  ".join(sunsinagents)
        else:
            cursor.close()
            conn.close()
            return ("모든 요원 입력 완료!")
    except Exception:
        cursor.close()
        conn.close()
        return ("조회 중 오류가 발생했습니다")

# 벌크 인서트
def bulk_insert():
    try:                                                   
        conn = get_connection()
        cursor = conn.cursor()
        df = pd.read_csv('note/menu.csv')
        start_idx = df.columns.get_loc('2025-01-07')
        mdf = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2], var_name='dt', value_name='menu')
        sdf=mdf.replace(["-","x","<결석>"], pd.NA)
        adf=sdf.dropna()
        blm = []
 

        members = {"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}

        success_cnt = 0
        fail_cnt = 0
            
        for i in adf.index:
            ename = adf.loc[i, "ename"]
            dt = adf.loc[i, "dt"]
            value = adf.loc[i, "menu"]
            blm.append((value,members[ename],dt))

        cursor.executemany("INSERT INTO lunch_menu (menu_name,member_id,dt) VALUES (%s,%s,%s) ON CONFLICT (member_id,dt)  DO NOTHING",blm)
        
        success_cnt = cursor.rowcount
        fail_cnt = len(blm) - success_cnt

        if success_cnt == len(blm):
            conn.commit()
            cursor.close()
            conn.close()
            return st.success(f" 벌크 인서트 완료 총 {success_cnt} 건")

        else:
            conn.commit()
            cursor.close()
            conn.close()
            return st.error(f"총 {len(blm)} 건 중 {fail_cnt} 건 실패")
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        print(f"Exception: {e}")
        return st.warning(f"오류 발생 ; {e}")

# 오늘 미입력자 전광판
def today_agents(tdd):
    query = """
        select
            m.name,count(l.id) as menc
        from
            member m
        left join lunch_menu l
        on
            l.member_id = m.id and l.dt = %s
        group by
            m.id, m.name
        having
            count(l.id) = 0
        order by
            menc desc"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query,(tdd,))
        rows = cursor.fetchall()
        fdf=pd.DataFrame(rows,columns=['name','count'])
        sunsinagents=fdf['name'].tolist()
        if len(sunsinagents) >=1:
            #st.text(",  ".join(sunsinagents))
            cursor.close()
            conn.close()
            return ",  ".join(sunsinagents)
        else:
            cursor.close()
            conn.close()
            return "모든 요원 입력 완료!"
    except Exception:
        cursor.close()
        conn.close()
        return "조회 중 오류가 발생했습니다"
