import sqlite3
from user import User

class UserRepository:
    def __init__(self, db_name: str = "user.db"):
        self.db_name = db_name
        self.create_table()
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    def create_table(self):
        with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                create table if not exists user(
                    user_id integer primary key,
                    name varchar(50) not null,
                    email varchar(250) not null,
                    role varchar(50) not null
                    )
                """)
                conn.commit()
    def list_all(self):
        with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("select * from user")
                rows = cursor.fetchall()
                return [User(row["user_id"], row["name"], row["email"], row["role"]) for row in rows]
    def find_by_id(self, user_id: int):
        with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    select * from user where user_id = ?
                """,(user_id,))
                row = cursor.fetchone()
                if row:
                    return User(row["user_id"], row["name"], row["email"], row["role"])
                return None 
    def add_user(self, user_data: User):
        with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    insert into user(user_id,name,email,role) values(?,?,?,?)
                """,
                (user_data.user_id, user_data.name, user_data.email, user_data.role)
                )
                conn.commit()
                return True
    def find_by_email(self, email: str):
        with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "select * from user where email = ?", (email,)
                )
                row = cursor.fetchone()
                if row:
                    return User(row["user_id"], row["name"], row["email"], row["role"])
                return None
    def update(self, user_id: int, new_name: str, new_email: str, new_role: str):
        with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    update user set name = ?, email = ?, role = ? 
                    where user_id =?
                """,(new_name,new_email,new_role,user_id))
                conn.commit()
                return cursor.rowcount > 0
    def delete(self,user_id: int):
        with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("delete from user where user_id = ?",(user_id,))
                conn.commit()
                return cursor.rowcount > 0  