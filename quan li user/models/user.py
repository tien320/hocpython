from datetime import date
from enum import Enum
from datetime import datetime
class Role(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
class Status(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BANNED = "BANNED"
class User:
    def __init__(self, 
                 user_id: int,
                 password: str, 
                 phone_number: str,
                 name: str, email: str, 
                 date_of_birth: date, 
                 role: Role = Role.USER, 
                 status: Status = Status.ACTIVE,
                 create_at: datetime | None = None, 
                 update_at:datetime | None = None):
        self.user_id = user_id
        self.password = password
        self.phone_number = phone_number
        self.name = name
        self.email = email
        self.date_of_birth = date_of_birth
        self.role = role
        self.status = status

        now = datetime.now()
        self.create_at = create_at if create_at is not None else now
        self.update_at = update_at if update_at is not None else now
    def __repr__(self) -> str:
        return f"User(id={self.user_id}, name='{self.name}', role='{self.role}')"