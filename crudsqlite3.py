import sqlite3
conn = sqlite3.connect("student.db")
cursor = conn.cursor()
try:
    cursor.execute("""
create table student(
id integer primary key,
name varchar(50) not null,
age int not null,
gpa real not null
)
""")
    print("đã tạo bảng")
except Exception as e:
    print(e)
try:
    cursor.execute("""
insert into student(id,name,age,gpa) values(1,"tien",23,3.2)
""")
    conn.commit()
    cursor.execute("""
select * from student     
""")
    print(cursor.fetchall())
    conn.commit()
except Exception as e:
    print(e)
try:
    cursor.execute("""
    update student set age = 22 where id = 1
    """)
    print("đã update")
    conn.commit()
except Exception as e:
    print(e)
