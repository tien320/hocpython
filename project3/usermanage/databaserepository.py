import sqlite3
from user import User
class DatabaseRepository:
    def __init__(self, db_name: str = "user.db"):
        self.db_name = db_name
    def get_connection(self, db_name: str):
        conn = sqlite3.connect("db_name")
        return conn
    def add(self):
        conn 


        
 