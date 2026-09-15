import threading
from contextlib import contextmanager
import oracledb
class Database:
    _instance = None
    _lock = threading.Lock()
    _initialize = False
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, user: str = "user",password: str = "123456",dsn: str = "localhost:1521/XEPDB1"):
        if not self._initialize:
            with self._lock:
                if not self._initialize:
                    self.user = user
                    self.password = password
                    self.dsn = dsn
                    self.pool = oracledb.create_pool(
                        user = self.user,
                        password = self.password,
                        dsn = self.dsn,
                        min = 2,
                        max = 10,
                        increment = 1
                    )
                    self._initialize = True
    @contextmanager
    def get_connection(self):
        conn = self.pool.acquire()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self.pool.release(conn)
    def close(self):
        if hasattr(self,"pool"):
            self.pool.close()