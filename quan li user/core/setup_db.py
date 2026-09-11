from core.database import db

def run_migrations():
    with db.get_connection() as conn:
        conn.cursor().executescript("""
            CREATE TABLE IF NOT EXISTS user (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS order (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
        """)
    print("Database và khóa ngoại đã được khởi tạo an toàn.")

if __name__ == "__main__":
    run_migrations()