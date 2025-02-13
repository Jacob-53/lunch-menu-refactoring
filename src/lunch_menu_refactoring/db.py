import streamlit as st
import pandas as pd
import psycopg
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import time
from datetime import datetime
import requests
import lunch_menu_refactoring.constants as const

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
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                        "INSERT INTO lunch_menu (menu_name,member_id,dt) VALUES (%s,%s,%s);",
                        (menu_name,member_id,dt)
                    )
                conn.commit()
                return True
    except Exception as e:
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
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()


            selected_df = pd.DataFrame(rows,columns=['menu','ename','dt'],index=range(1,len(rows)+1))
        
            return selected_df
# 입력 횟수 출력
def count_member():
    query="""SELECT
        lunch_menu.menu_name AS menu,
        member.name AS ename,
        lunch_menu.dt, member.id
        FROM member
        INNER JOIN lunch_menu ON member.id = lunch_menu.member_id
        ORDER BY lunch_menu.dt DESC"""
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            df = pd.DataFrame(rows,columns=['menu','ename','dt','id'],index=range(1,len(rows)+1))
            fdf = df.groupby(['ename','id'])['menu'].count().reset_index().set_index('id')
            sdf = fdf.sort_values(by='menu', ascending=False)
            adf = sdf.style.set_properties(color="green", align="left")
            return adf
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
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

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
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(queryy,(cdt,))
                rowss = cursor.fetchall()
                fdf=pd.DataFrame(rowss,columns=['name','count'])
                sunsinagents=fdf['name'].tolist()
                if len(sunsinagents) >=1:
                    #st.text(",  ".join(sunsinagents))
                    return ",  ".join(sunsinagents)
                else:
                    return ("모든 요원 입력 완료!")
    except Exception:
        return ("조회 중 오류가 발생했습니다")

# 벌크 인서트
def bulk_insert():
    try:                                                   
        with get_connection() as conn:
            with conn.cursor() as cursor:
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
                    return st.success(f" 벌크 인서트 완료 총 {success_cnt} 건")

                else:
                    return st.error(f"총 {len(blm)} 건 중 {fail_cnt} 건 실패")
    except Exception as e:
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
        with get_connection() as conn:
            with conn.cursor() as cursor:        
                cursor.execute(query,(tdd,))
                rows = cursor.fetchall()
                fdf=pd.DataFrame(rows,columns=['name','count'])
                sunsinagents=fdf['name'].tolist()
                if len(sunsinagents) >=1:
                #st.text(",  ".join(sunsinagents))
                    return ",  ".join(sunsinagents)
                else:
                    return "모든 요원 입력 완료!"
    except Exception:
        return "조회 중 오류가 발생했습니다"

#요일별 TOP3 메뉴
def date_menu(dat:str):
    num_convert = {
        '일요일': 0,
        '월요일': 1,
        '화요일': 2,
        '수요일': 3,
        '목요일': 4,
        '금요일': 5,
        '토요일': 6
    }
    date_number = num_convert.get(dat)
    query = f"""
        select menu_name,count(menu_name),dt,extract(dow FROM dt::date)
        FROM lunch_menu 
        where  extract(dow FROM dt::date) = {date_number}
        group by menu_name,dt,extract(dow FROM dt::date)
        order by count(menu_name) desc
        limit 3;"""

    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                if not rows:
                    return " 해당 일의 데이터가 없습니다"
                df=pd.DataFrame(rows,columns=['menu_name','count','dt','dow'],index=range(1,len(rows)+1))
                adf=df[['menu_name', 'count']]
                #sdf=adf.loc[:,['menu_name','dt']]
                return adf
    except Exception:
        return "조회 중 오류가 발생했습니다"

#메뉴 인기 순위
def top_pick_menu():
    query = """
        select menu_name,count(menu_name)
from lunch_menu
group by lunch_menu.menu_name 
order by count(menu_name) desc
limit 10"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                if not rows:
                    return "입력된 데이터가 없어 출력 할 수 없습니다"
                df=pd.DataFrame(rows,columns=['menu_name','count'],index=range(1,len(rows)+1))
                fdf = df.style.set_properties(color="red", align="left")
                return fdf 

    except Exception:
        return "조회 중 오류가 발생했습니다"


#Api Sync
def api_sync():
    ep = f"{const.ppabam_url}"
    res = requests.get(ep)
    datamain = res.json()
    endpoint = datamain['endpoints']
    del endpoint[4:6]
    syncmem = [(i['name'],i['url']) for i in endpoint]
    sync_list=[]
    for i in range(len(syncmem)):
        resmem = requests.get(syncmem[i][1])
        data = resmem.json()
        df1 = pd.DataFrame(data)
        df1 = df1.astype(str).apply(lambda col: col.map(str.lower))#lambda 사용 소문자통일
        resme = requests.get(f"{const.jacob_req_url}")
        datame = resme.json()
        dfme = pd.DataFrame(datame)
        dfme = dfme.astype(str).apply(lambda col: col.map(str.lower))
        merge_df = pd.merge(df1, dfme, on=["dt","name"], how="left", indicator=True)
        df_diff_1 = merge_df[merge_df['_merge'] == 'left_only'].drop(['_merge','menu_name_y'] , axis=1)
        df_sync = df_diff_1.sort_values(by=['name']).reset_index(drop=True)
        if "menu_name" not in df_sync.columns and "menu_name_x" in df_sync.columns:#컬럼명 변경
            df_sync.rename(columns={"menu_name_x":"menu_name"},inplace=True)
        if not df_sync.empty:
            for row in df_sync.itertuples(index=False):
                sync_list.append(tuple(row))

    members = {"seo": 5, "tom": 1, "cho": 2, "hyun": 3, "nuni": 10, "jerry": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}
    sync_list=[(i[0],members.get(i[1], i[1]),i[2]) for i in sync_list]
    #for i in sync_list:
    #   sync_list.append((i[0],members[i[1]],i[2])) 같은 결과
    distinct_list=list(set(sync_list))
    r_cnt = len(sync_list)-len(distinct_list)
    try:                                                   
        with get_connection() as conn:
            with conn.cursor() as cursor:
                success_cnt = 0
                fail_cnt = 0
                cursor.executemany("INSERT INTO lunch_menu (menu_name,member_id,dt) VALUES (%s,%s,%s) ON CONFLICT (member_id,dt)  DO NOTHING",distinct_list)
        
                success_cnt = cursor.rowcount
                fail_cnt = len(distinct_list) - success_cnt

                if len(distinct_list) == 0 :
                    st.balloons()
                    return st.success(f"이미 최신화 되어 있습니다")
                elif success_cnt == len(distinct_list):
                    st.balloons()
                    return st.success(f""" 작업완료 - 새로운 원천 {len(syncmem)} 곳에서 총 {success_cnt} 건 추가 하였습니다.
                                      총{len(sync_list)}건 중 중복 값 {r_cnt} 건 """) 
                else:
                    return st.error(f"총 {len(distinct_list)} 건 중 {fail_cnt} 건 실패")
    except Exception as e:
        print(f"Exception: {e}")
        return st.warning(f"오류 발생 ; {e}")
    
#Api Status
def check_api():
    ep = f"{const.ppabam_url}"
    res = requests.get(ep)
    datamain = res.json()
    endpoint = datamain['endpoints']
    syncmem = [(i['name'],i['url']) for i in endpoint]
    status_list=[]
    for name,url in syncmem:
        try:
            response = requests.get(url)
            status = response.status_code
            if status == 200:
                status_list.append(f"🟢 {name}:{status}")
            else:
                status_list.append(f"🔴 {name}:{status}")
        except Exception as e:
            status_list.append(f"Error {e}")
    st.balloons()       
    return status_list
