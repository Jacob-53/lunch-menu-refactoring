# 🍽️ **lunch-menu**

- [x] 팀원들의 점심 메뉴를 수집
- [x] 분석
- [x] 알람(입력하지 않은 사람들에게 ...)
- [x] CSV to DB

---

## 🛠️ **Ready**

### 📦 **Install DB with Docker**

```bash
$ sudo docker run --name local-postgres \
-e POSTGRES_USER=sunsin \
-e POSTGRES_PASSWORD=mysecretpassword \
-e POSTGRES_DB=sunsindb \
-p 5432:5432 \
-d postgres:15.10
```

### 🗂️ **Create Table**

- PostgreSQL:
```sql
CREATE TABLE public.member (
	id serial4 NOT NULL,
	"name" text NOT NULL,
	CONSTRAINT member_id_pk PRIMARY KEY (id),
	CONSTRAINT member_name_key UNIQUE (name)
);

insert into public.member(name)
values 
('TOM'),
('cho'),
('hyun'),
('JERRY'),
('SEO'),
('jiwon'),
('jacob'),
('heejin'),
('lucas'),
('nuni');

CREATE TABLE public.lunch_menu (
	id serial4 NOT NULL,
	menu_name text NOT NULL,
	dt date NOT NULL,
	member_id int4 NOT NULL,
	CONSTRAINT lunch_menu_pk PRIMARY KEY (id),
	CONSTRAINT unique_memberid_dt UNIQUE (member_id, dt)
);

-- public.lunch_menu foreign keys
ALTER TABLE public.lunch_menu ADD CONSTRAINT menu_member_fk FOREIGN KEY (member_id) REFERENCES public.member(id);
```

<details>
<summary>📚 **누적 생성 (SQL 블록)**</summary>

```sql
CREATE TABLE public.lunch_menu (
	id serial NOT NULL,
	menu_name text NOT NULL,
	member_name text NOT NULL,
	dt date NOT NULL,
	CONSTRAINT lunch_menu_pk PRIMARY KEY (id)
);

alter table lunch_menu
add constraint unique_member_dt unique (member_name, dt);

create table member(
id serial NOT NULL,
name text unique NOT NULL
);

insert into member(name)
values 
('TOM'),
('cho'),
('hyun'),
('JERRY'),
('SEO'),
('jiwon'),
('jacob'),
('heejin'),
('lucas'),
('nuni');

SELECT jsonb_object_agg(name, id) 
FROM (
	select name, id from member order by id
) temp;

{"SEO": 5, "TOM": 1, "cho": 2, "hyun": 3, "nuni": 10, "JERRY": 4, "jacob": 7, "jiwon": 6, "lucas": 9, "heejin": 8}

-- 새로운 컬럼 추가
alter table lunch_menu 
add column member_id int;

select * from lunch_menu limit 1;

-- 기존의 제약조건을 삭제
alter table lunch_menu
drop constraint unique_member_dt;

-- 사용하지 않는 컬럼 삭제
alter table lunch_menu 
drop column member_name;

-- member_id null 값을 허용하지 않도록 설정
-- delete from lunch_menu;
alter table lunch_menu
alter column member_id set not null;

-- 새로운 제약조건 추가
alter table lunch_menu
add constraint unique_memberid_dt unique (member_id, dt);

-- 맵버 테이블에 기본키를 설정
alter table member
add constraint member_id_pk primary key(id);

-- 관계 조건 추가
alter table lunch_menu
add constraint menu_member_fk 
	foreign key (member_id)
	REFERENCES  member(id)
;
-- SQL Error [42830]: ERROR: there is no unique constraint matching given keys for referenced table "member"

-- 테스트
select * from member;
select max(id) from member; -- 10

insert into lunch_menu(menu_name, member_id, dt)
values('순대국', 1, '2025-01-01');

select * from lunch_menu;

insert into lunch_menu(menu_name, member_id, dt)
values('순대국', 11, '2025-01-01');
-- SQL Error [23503]: ERROR: insert or update on table "lunch_menu" violates foreign key constraint "menu_member_fk"
```

</details>

---

## 💻 **Dev**

### 🐳 **DB 관리**

```bash
$ sudo docker ps -a
$ sudo docker start local-postgres
$ sudo docker stop local-postgres

# Into CONTAINER
$ sudo docker exec -it local-postgres bash
```

### 🚀 **RUN**

```bash
# 디비 정보에 맞춰 수정
$ cp env.dummy .env

# 서버 시작
$ streamlit run Main.py# lunch-menu-refactoring
