import threading
from contextlib import contextmanager
import oracledb
from core.config import settings

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
    def __init__(self):
        if not self._initialize:
            with self._lock:
                if not self._initialize:
                    self.pool = oracledb.create_pool(
                        user = settings.DB_USER,
                        password = settings.DB_PASSWORD,
                        dsn = settings.DB_DSN,
                        min = settings.DB_POOL_MIN,
                        max = settings.DB_POOL_MAX,
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