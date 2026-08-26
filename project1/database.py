import sqlite3
class DatabaseConnection:
    def __init__(self,db_name:str="store.db"):
        self.db_name = db_name
        self.conn = None
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    def __exit__(self, exc_type, exc, tb):
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()
    # Thêm vào cuối file database.py
# Thêm vào cuối file database.py
def init_db():
    with DatabaseConnection("store.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                total_price REAL NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)