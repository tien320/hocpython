import oracledb
from models.user import UserCreate, UserResponse, UserRole
from core.database import Database

class UserRepository:
    def __init__(self, db: Database | None = None):
        self.db = db if db is not None else Database()

    def add(self, user: UserCreate, role: UserRole = UserRole.USER) -> UserResponse:
        query = """
            INSERT INTO users (name, email, phone_number, password, role)
            VALUES (:name, :email, :phone_number, :password, :role)
            RETURNING user_id INTO :out_user_id
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                out_user_id = cursor.var(oracledb.NUMBER)
                cursor.execute(query, {
                    "name": user.name,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "password": user.password,
                    "role": role.value,
                    "out_user_id": out_user_id
                })
                new_id = int(out_user_id.getvalue()[0])
                
                return UserResponse(
                    user_id=new_id,
                    name=user.name,
                    email=user.email,
                    phone_number=user.phone_number,
                    role=role
                )

    def list_all(self) -> list[UserResponse]:
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT user_id, name, email, phone_number, role FROM users")
                col_names = [col[0].lower() for col in cursor.description]
                rows = cursor.fetchall()
                return [self._map_row_to_response(dict(zip(col_names, row))) for row in rows]

    def find_by_id(self, user_id: int) -> UserResponse | None:
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT user_id, name, email, phone_number, role FROM users WHERE user_id = :id", [user_id])
                row = cursor.fetchone()
                if not row:
                    return None
                col_names = [col[0].lower() for col in cursor.description]
                return self._map_row_to_response(dict(zip(col_names, row)))

    def find_by_email(self, email: str) -> dict | None:
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT user_id, name, email, phone_number, password, role FROM users WHERE email = :email", [email])
                row = cursor.fetchone()
                if not row:
                    return None
                col_names = [col[0].lower() for col in cursor.description]
                return dict(zip(col_names, row))

    def update(self, user_id: int, user: UserCreate, role: str = "user") -> bool:
        query = """
            UPDATE users 
            SET name = :name, email = :email, phone_number = :phone_number, password = :password, role = :role 
            WHERE user_id = :user_id
        """
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {
                    "name": user.name,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "password": user.password,
                    "role": role,
                    "user_id": user_id
                })
                return cursor.rowcount > 0

    def delete(self, user_id: int) -> bool:
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE user_id = :user_id", [user_id])
                return cursor.rowcount > 0

    def _map_row_to_response(self, data: dict) -> UserResponse:
        return UserResponse(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],
            phone_number=data["phone_number"],
            role=UserRole(data.get("role", "user"))
        )