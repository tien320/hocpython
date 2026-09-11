from core.database import Database
from models.user import User
from datetime import date, datetime
from models.user import Role, Status
class UserRepository:
    def __init__(self, db: Database | None = None):
        self.db = db if db is not None else Database()
    def list_all(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("select * from user")
            rows = cursor.fetchall()
            return [self._map_row_to_user(row) for row in rows]
    def find_by_id(self, user_id: int):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("select * from user where user_id =?",(user_id,))
            row =cursor.fetchone()
            return self._map_row_to_user(row) if row else None
    def add(self,user: User):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user (
                        password, phone_number, name, email, 
                        date_of_birth, role, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user.password,
            user.phone_number,
            user.name,
            user.email,
            user.date_of_birth.isoformat() if isinstance(user.date_of_birth, date) else user.date_of_birth,
            user.role.value if isinstance(user.role, Role) else user.role,
            user.status.value if isinstance(user.status, Status) else user.status,
            user.create_at.isoformat() if isinstance(user.create_at, datetime) else user.create_at,
            user.update_at.isoformat() if isinstance(user.update_at, datetime) else user.update_at,))
            return cursor.rowcount > 0 
    def update(self, user_id: int ,name: str, phone_number: str, role: Role, status: Status):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                    UPDATE user 
                    SET name = ?, phone_number = ?, role = ?, status = ?, updated_at = ?
                    WHERE user_id = ?
                    """,
                (
                    name,
                    phone_number,
                    role.value if isinstance(role, Role) else role,
                    status.value if isinstance(status, Status) else status,
                    datetime.now().isoformat(),
                    user_id
                )
            )
            return cursor.rowcount > 0
    def delete(self, user_id: int):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("delete from user where user_id =?",(user_id,))
            return cursor.rowcount > 0
    def _map_row_to_user(self, row) -> User:
        """Hàm trợ giúp chuyển đổi Row SQLite thành Object User."""
        return User(
            user_id=row["user_id"],
            password=row["password"],
            phone_number=row["phone_number"],
            name=row["name"],
            email=row["email"],
            date_of_birth=date.fromisoformat(row["date_of_birth"]) if isinstance(row["date_of_birth"], str) else row["date_of_birth"],
            role=Role(row["role"]),
            status=Status(row["status"]),
            create_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
            update_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None,
        )
        