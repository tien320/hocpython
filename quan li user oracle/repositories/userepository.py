from models.user import User
from core.database import Database
class UserRepository:
    def __init__(self, db: Database| None = None):
        self.db = db if db is not None else Database()
    def add(self, user: User):
      with self.db.get_connection() as conn:
         with conn.cursor() as cursor:
            cursor.execute("insert into users(user_id,name,password,phone_number,email) values(:user_id, :name, :password, :phone_number, :email)",{
               "user_id" : user.user_id,
               "name": user.name,
               "password": user.password,
               "phone_number": user.phone_number,
               "email": user.email
            })
            return cursor.rowcount > 0
    def list_all(self):
       with self.db.get_connection() as conn:
          with conn.cursor() as cursor:
             cursor.execute("select * from users")
             col_names = [col[0].lower() for col in cursor.description]
             rows = cursor.fetchall()
             return [self._map_row_to_user(dict(zip(col_names,row))) for row in rows]
    def find_by_id(self,user_id: int):
       with self.db.get_connection() as conn:
          with conn.cursor() as cursor:
             cursor.execute("select * from users where user_id = :id", id = user_id)
             row = cursor.fetchone()
             if not row: return None
             col_names = [col[0].lower() for col in cursor.description]
             return self._map_row_to_user(dict(zip(col_names,row)))
    def update(self,user: User):
       with self.db.get_connection() as conn:
          with conn.cursor() as cursor:
             cursor.execute("update users set name = :name, password = :password, phone_number = :phone_number, email= :email where user_id = :user_id",
                {
                   "name": user.name,
                   "password": user.password,
                   "phone_number": user.phone_number,
                   "email": user.email,
                   "user_id": user.user_id
             })
             return cursor.rowcount > 0
    def delete(self, user_id: int):
       with self.db.get_connection() as conn:
          with conn.cursor() as cursor:
             cursor.execute("delete from users where user_id = :user_id",user_id=user_id)
             return cursor.rowcount > 0
    def _map_row_to_user(self, data: dict):
       return User(
          user_id = data["user_id"],
          password = data["password"],
          name = data["name"],
          phone_number = data["phone_number"],
          email=data["email"]
       )