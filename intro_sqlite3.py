import sqlite3
conn = sqlite3.connect("test_db")
cursor = conn.cursor()
cursor.execute("""
    create table student(
        student_id integer primary key,
        name text not null,
        age integer not null,
        gpa real not null
    )
""")
conn.commit()
print("đã tạo bảng")
student_data = (1,"tiến",21,3.4)
cursor.execute("""
    insert into student(student_id,name,age,gpa) values(?,?,?,?)
""",
    student_data
)
conn.commit()
print("đã thêm dữ liệu")
cursor.execute("select * from student")
all_row = cursor.fetchall()
for row in all_row:
    print(row)
cursor.execute("select * from student where student_id = 1")
all_row = cursor.fetchall()
for row in all_row:
    print(row)
students_data = [
    (2, "Nguyễn Văn An", 20, 3.20),
    (3, "Trần Thị Bình", 19, 3.85),
    (4, "Phạm Minh Cường", 22, 2.75),
    (5, "Hoàng Lan Dung", 20, 3.40),
    (6, "Vũ Đức Giang", 21, 3.90),
    (7, "Đỗ Khánh Huyền", 19, 3.15),
    (8, "Bùi Quang Khải", 23, 2.95),
    (9, "Ngô Phương Linh", 20, 3.70),
    (10, "Đặng Tuấn Nam", 21, 3.55)
]
cursor.executemany("""
    insert into student(student_id,name,age,gpa) values(?,?,?,?)
""",
    students_data
)
conn.commit()
cursor.execute("select * from student where student_id =1")
all_row = cursor.fetchall()
for row in all_row:
    print(row)
cursor.execute("""
    update student 
    set gpa = 3.8
    where student_id = 1
""")
conn.commit()
print("đã update dữ liệu")
cursor.execute("select gpa from student where student_id = 1")
print(cursor.fetchone())
cursor.execute("""
    delete from student 
    where student_id = 2
""")
conn.commit()
print("đã xóa")
conn.close()