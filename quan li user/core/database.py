import sqlite3
class Database:
    _instance = None
    _initialize = False
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, db_name: str = "identity.db"):
        if not self._initialize:
            self.db_name = db_name
            self._initialize = True
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
db = Database()

        