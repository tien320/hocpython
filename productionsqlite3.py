import sqlite3

def get_db_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path, timeout=10.0) # Tránh lỗi "database locked" khi chờ ghi
    conn.row_factory = sqlite3.Row              # Cho phép truy cập cột dạng dict: row["name"]
    
    # Kích hoạt WAL mode để đọc và ghi diễn ra đồng thời
    conn.execute("PRAGMA journal_mode=WAL;")
    # Bật ràng buộc khóa ngoại (SQLite mặc định tắt)
    conn.execute("PRAGMA foreign_keys=ON;")
    # Cân bằng giữa an toàn dữ liệu và tốc độ ghi
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn
import logging
import sqlite3
from contextlib import contextmanager
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, db_path: str):
        self.db_path = db_path

    @contextmanager
    def _get_connection(self):
        """Context manager tự động commit khi thành công và rollback khi gặp lỗi."""
        conn = get_db_connection(self.db_path)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.exception("Lỗi transaction DB: %s", e)
            raise
        finally:
            conn.close()

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, age FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def create(self, name: str, email: str, age: int) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                (name, email, age)
            )
            return cursor.lastrowid